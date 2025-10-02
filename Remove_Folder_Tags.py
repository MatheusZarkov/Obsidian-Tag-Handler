import os
import yaml
import re

def get_all_folder_names(base_dir):
    """Get all folder names in the directory tree"""
    folder_names = set()
    for root, dirs, files in os.walk(base_dir):
        # Skip .obsidian folder
        if '.obsidian' in dirs:
            dirs.remove('.obsidian')
        
        for dir_name in dirs:
            folder_names.add(dir_name)
    
    return folder_names

def remove_folder_tags_from_file(file_path, folder_names):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Check if the file has YAML front matter
        yaml_pattern = r'^---\n(.*?)\n---'
        yaml_match = re.match(yaml_pattern, content, re.DOTALL)
        
        if yaml_match:
            try:
                # Parse existing YAML
                existing_yaml = yaml.safe_load(yaml_match.group(1))
                if existing_yaml and 'tags' in existing_yaml:
                    original_tags = existing_yaml['tags']
                    
                    # Handle both list and single string tags
                    if isinstance(original_tags, list):
                        # Remove tags that match folder names
                        filtered_tags = [tag for tag in original_tags if tag not in folder_names]
                        
                        if len(filtered_tags) != len(original_tags):  # Something was removed
                            if filtered_tags:  # Still have tags left
                                existing_yaml['tags'] = filtered_tags
                            else:  # No tags left, remove the tags property
                                del existing_yaml['tags']
                            
                            # Update the content
                            if existing_yaml:
                                new_yaml_string = yaml.dump(existing_yaml, allow_unicode=True, sort_keys=False)
                                new_content = f"---\n{new_yaml_string}---\n{content[yaml_match.end():].lstrip()}"
                            else:
                                # If no other YAML properties, remove the entire front matter
                                new_content = content[yaml_match.end():].lstrip()
                            
                            # Write the modified content back
                            with open(file_path, 'w', encoding='utf-8') as file:
                                file.write(new_content)
                            
                            removed_tags = [tag for tag in original_tags if tag in folder_names]
                            print(f"Removed folder tags {removed_tags} from: {file_path}")
                            return True
                    
                    elif isinstance(original_tags, str):
                        # Single tag as string
                        if original_tags in folder_names:
                            del existing_yaml['tags']
                            
                            if existing_yaml:
                                new_yaml_string = yaml.dump(existing_yaml, allow_unicode=True, sort_keys=False)
                                new_content = f"---\n{new_yaml_string}---\n{content[yaml_match.end():].lstrip()}"
                            else:
                                new_content = content[yaml_match.end():].lstrip()
                            
                            with open(file_path, 'w', encoding='utf-8') as file:
                                file.write(new_content)
                            
                            print(f"Removed folder tag '{original_tags}' from: {file_path}")
                            return True
                
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {file_path}: {e}")
                return False
    
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False
    
    return False

def process_directory(base_dir):
    # First, get all folder names
    folder_names = get_all_folder_names(base_dir)
    print(f"Found folders: {sorted(folder_names)}")
    
    files_processed = 0
    files_changed = 0
    
    for root, dirs, files in os.walk(base_dir):
        # Skip .obsidian folder
        if '.obsidian' in dirs:
            dirs.remove('.obsidian')
        
        for file in files:
            if file.endswith('.md'):
                files_processed += 1
                file_path = os.path.join(root, file)
                if remove_folder_tags_from_file(file_path, folder_names):
                    files_changed += 1

    # Print summary
    print(f"\nSummary:")
    print(f"Files processed: {files_processed}")
    print(f"Files modified (folder tags removed): {files_changed}")

if __name__ == "__main__":
    # Get the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Confirmation prompt
    print("This script will remove tags that match folder names from your Markdown files.")
    print("This action cannot be undone.")
    response = input("Do you want to continue? (yes/no): ")
    
    if response.lower() == 'yes':
        process_directory(script_directory)
    else:
        print("Operation cancelled.")
