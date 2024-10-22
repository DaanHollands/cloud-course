import yaml
import os

def get_all_files(folder_path):
    # List to store relative file paths
    file_paths = []
    # Walk through all subdirectories and files
    for root, _, files in os.walk(folder_path):
        for file in files:
            # Create the relative file path
            relative_path = os.path.relpath(os.path.join(root, file), folder_path)
            file_paths.append(relative_path)
    return file_paths

def read_front_matter(file_path):
    with open(file_path, 'r') as file:
        # Read the content of the file
        content = file.read()
        # Split the content to extract front matter
        if content.startswith('---'):
            _, front_matter, _ = content.split('---', 2)
            # Parse the front matter using yaml
            data = yaml.safe_load(front_matter)
            return data
        else:
            return None

def get_files_with_weights(folder_path):
    # Dictionary to store file paths and their weights
    files_weights = {}
    # Get all the files in the folder
    all_files = get_all_files(folder_path)
    # Loop through the files and get their weights from the front matter
    for file in all_files:
        # Construct the full file path
        full_path = os.path.join(folder_path, file)
        # Read the front matter
        front_matter_data = read_front_matter(full_path)
        # If front matter exists and has a weight, add it to the dictionary
        if front_matter_data and 'weight' in front_matter_data:
            files_weights[folder_path + file] = front_matter_data['weight']
    return files_weights

def sort_files_by_weight(files_weights):
    # Sort the dictionary by weight
    sorted_files = dict(sorted(files_weights.items(), key=lambda item: item[1]))
    return sorted_files

def concatenate_files(sorted_files):
    combined_content = ""
    # Loop through the sorted files
    for file in sorted_files:
        # Read the entire content of each file
        with open(file, 'r') as f:
            file_content = f.read()
            # Concatenate the content
            combined_content += file_content + "\n"
    return combined_content

def save_to_output_file(output_path, content):
    # Save the combined content to an output file
    with open(output_path, 'w') as output_file:
        output_file.write(content)

folder_path = 'content/Applicatiecolleges/'  # Replace 'your_folder' with the path to your folder
output_file_path = 'output.md'

files_with_weights = get_files_with_weights(folder_path)
sorted_files = sort_files_by_weight(files_with_weights)
combined_content = concatenate_files(sorted_files)
save_to_output_file(output_file_path, combined_content)