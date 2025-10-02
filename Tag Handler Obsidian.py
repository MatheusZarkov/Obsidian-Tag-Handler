import os
import yaml
import re

def get_nested_path_tag(file_path, script_directory):
    """Generate a single nested tag from the full folder path"""
    # Get the relative path from the script directory
    rel_path = os.path.relpath(file_path, script_directory)
    # Split the path and remove the file name
    path_parts = os.path.dirname(rel_path).split(os.sep)
    # Filter out empty parts and replace spaces with underscores
    clean_parts = [part.replace(' ', '_') for part in path_parts if part and part != '.']
    
    if clean_parts:
        # Return single nested tag with all folder levels
        return '/'.join(clean_parts)
    return None

def get_all_possible_path_tags(script_directory):
    """Get all possible path tags from the directory structure"""
    path_tags = set()
    for root, dirs, _ in os.walk(script_directory):
        # Skip .obsidian folder
        if '.obsidian' in dirs:
            dirs.remove('.obsidian')
        
        # Get relative path parts
        rel_path = os.path.relpath(root, script_directory)
        if rel_path == '.':
            continue
            
        path_parts = rel_path.split(os.sep)
        clean_parts = [part.replace(' ', '_') for part in path_parts if part]
        
        if clean_parts:
            # Add the full nested path as a single tag
            nested_tag = '/'.join(clean_parts)
            path_tags.add(nested_tag)
    
    return path_tags

def is_path_tag(tag, all_path_tags):
    """Check if a tag represents a folder path structure"""
    return tag in all_path_tags

def process_file(file_path, script_directory, all_path_tags):
    changes = []  # List to store changes
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return

    # Check if the file already has YAML front matter
    yaml_pattern = r'^---\n(.*?)\n---'
    yaml_match = re.match(yaml_pattern, content, re.DOTALL)
    
    # Get current path tag
    current_path_tag = get_nested_path_tag(file_path, script_directory)
    
    if yaml_match:
        # If YAML front matter exists
        try:
            existing_yaml = yaml.safe_load(yaml_match.group(1))
            if existing_yaml is None:
                existing_yaml = {}
            
            # Get existing tags or create empty list
            existing_tags = existing_yaml.get('tags', [])
            if isinstance(existing_tags, str):
                existing_tags = [existing_tags]
            elif existing_tags is None:
                existing_tags = []
            
            # Separate custom tags from old path tags
            custom_tags = []
            old_path_tags = []
            
            for tag in existing_tags:
                if is_path_tag(tag, all_path_tags):
                    old_path_tags.append(tag)
                else:
                    custom_tags.append(tag)
            
            # Create new tag list: custom tags + current path tag
            new_tags = custom_tags.copy()
            if current_path_tag:
                new_tags.append(current_path_tag)
            
            # Remove duplicates and sort
            new_tags = list(set(new_tags))
            new_tags.sort()
            
            # Track changes
            if current_path_tag and current_path_tag not in existing_tags:
                changes.append(f"Added path tag: {current_path_tag}")
            
            if old_path_tags:
                # Check if the old path tags are different from current
                if not current_path_tag or current_path_tag not in old_path_tags:
                    changes.append(f"Removed old path tags: {', '.join(old_path_tags)}")
            
            # Update YAML with all existing properties
            existing_yaml['tags'] = new_tags
            
            # Preserve the order of existing YAML properties
            new_yaml_string = yaml.dump(existing_yaml, allow_unicode=True, sort_keys=False)
            
            # Get the content after front matter and clean up extra newlines
            remaining_content = content[yaml_match.end():].lstrip()
            
            # Combine the front matter with content
            new_content = f"---\n{new_yaml_string}---\n{remaining_content}"
            
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {file_path}: {e}")
            return
    else:
        # If no YAML front matter exists, create new one
        if current_path_tag:
            new_yaml = {'tags': [current_path_tag]}
            new_yaml_string = yaml.dump(new_yaml, allow_unicode=True, sort_keys=False)
            content = content.lstrip()
            new_content = f"---\n{new_yaml_string}---\n{content}"
            changes.append(f"Added initial path tag: {current_path_tag}")
        else:
            # If no path tag needed, don't modify the file
            return

    # Only write to file if there were changes
    if changes:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            # Get relative path for cleaner output
            rel_path = os.path.relpath(file_path, script_directory)
            print(f"\nFile: {rel_path}")
            for change in changes:
                print(f"  {change}")
                
        except Exception as e:
            print(f"Error writing to file {file_path}: {e}")


def process_directory(base_dir):
    # Get all possible path tags first
    all_path_tags = get_all_possible_path_tags(base_dir)
    
    files_processed = 0
    
    # Process all markdown files in the directory tree
    for root, dirs, files in os.walk(base_dir):
        # Skip .obsidian folder
        if '.obsidian' in dirs:
            dirs.remove('.obsidian')
        
        for file in files:
            if file.endswith('.md'):
                files_processed += 1
                file_path = os.path.join(root, file)
                process_file(file_path, base_dir, all_path_tags)
                
    print(f"\nSummary:")
    print(f"Files processed: {files_processed}")

if __name__ == "__main__":
    # Get the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    process_directory(script_directory)