import os
import yaml
import re

def get_path_tags(file_path, script_directory):
    # Get the relative path from the script directory
    rel_path = os.path.relpath(file_path, script_directory)
    # Split the path and remove the file name
    path_parts = os.path.dirname(rel_path).split(os.sep)
    # Only keep the first two parts (parent folder and first subfolder)
    tags = [part.replace(' ', '_') for part in path_parts[:2] if part]
    return tags

def get_all_possible_folder_tags(script_directory):
    """Get all possible folder tags from the directory structure"""
    folder_tags = set()
    for root, dirs, _ in os.walk(script_directory):
        # Skip .obsidian folder
        if '.obsidian' in dirs:
            dirs.remove('.obsidian')
        
        # Get relative path parts
        rel_path = os.path.relpath(root, script_directory)
        if rel_path == '.':
            continue
            
        path_parts = rel_path.split(os.sep)
        # Add only first two levels of folders
        for part in path_parts[:2]:
            folder_tags.add(part.replace(' ', '_'))
    
    return folder_tags

def process_file(file_path, script_directory, folder_tags):
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
    
    # Get current path tags
    current_path_tags = get_path_tags(file_path, script_directory)
    
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
            
            # Remove old folder tags but keep custom tags
            custom_tags = [tag for tag in existing_tags if tag not in folder_tags]
            
            # Combine custom tags with new path tags
            all_tags = list(set(custom_tags + current_path_tags))
            all_tags.sort()  # Optional: sort tags alphabetically
            
            # Track changes
            added_tags = [tag for tag in all_tags if tag not in existing_tags]
            removed_tags = [tag for tag in existing_tags if tag not in all_tags]
            
            if added_tags:
                changes.append(f"Added tags: {', '.join(added_tags)}")
            if removed_tags:
                changes.append(f"Removed tags: {', '.join(removed_tags)}")
            
            # Create new YAML front matter
            new_yaml = {'tags': all_tags}
            new_yaml_string = yaml.dump(new_yaml, allow_unicode=True, sort_keys=False)
            
            # Get the content after front matter and clean up extra newlines
            remaining_content = content[yaml_match.end():].lstrip()
            
            # Combine the front matter with content
            new_content = f"---\n{new_yaml_string}---\n{remaining_content}"
            
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {file_path}: {e}")
            return
    else:
        # If no YAML front matter exists, create new one
        new_yaml = {'tags': current_path_tags}
        new_yaml_string = yaml.dump(new_yaml, allow_unicode=True, sort_keys=False)
        content = content.lstrip()
        new_content = f"---\n{new_yaml_string}---\n{content}"
        changes.append(f"Added initial tags: {', '.join(current_path_tags)}")

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
    # Get all possible folder tags first
    folder_tags = get_all_possible_folder_tags(base_dir)
    
    files_processed = 0
    files_changed = 0
    
    # Process only the immediate subdirectories in the base directory
    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        
        # Skip the script file itself and the .obsidian folder
        if item == '.obsidian' or item.endswith('.py'):
            continue
            
        if os.path.isdir(full_path):
            # Walk through each subdirectory
            for root, dirs, files in os.walk(full_path):
                # Remove .obsidian folder from dirs if present
                if '.obsidian' in dirs:
                    dirs.remove('.obsidian')
                
                for file in files:
                    if file.endswith('.md'):
                        files_processed += 1
                        file_path = os.path.join(root, file)
                        process_file(file_path, base_dir, folder_tags)
                        files_changed += 1

    # Print summary
    print(f"\nSummary:")
    print(f"Files processed: {files_processed}")
    print(f"Files changed: {files_changed}")

if __name__ == "__main__":
    # Get the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    process_directory(script_directory)