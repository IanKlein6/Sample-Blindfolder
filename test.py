import os
import random

def create_test_folders(base_dir, num_folders, num_files_per_folder):
    # Define a list of file extensions
    extensions = ['png']

    # Ensure the base directory exists
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Loop to create folders
    for i in range(1, num_folders + 1):
        folder_name = f"folder{i}"
        folder_path = os.path.join(base_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Loop to create files within each folder
        for j in range(1, num_files_per_folder + 1):
            # Choose a random extension for each file
            ext = random.choice(extensions)
            # Adjust the filename pattern as per your requirement
            file_name = f"240317_814×{i + 29}_pyd_31_#31_{j}.{ext}"
            file_path = os.path.join(folder_path, file_name)

            # Create a file with sample content
            with open(file_path, 'w') as f:
                f.write("Sample content")

# Example usage: create 5 folders, each with 10 files
create_test_folders(os.getcwd(), 5, 10)
