import os
import random
import logging
import pandas as pd
import shutil

def sort_key(filename):
    """Custom sorting key to sort filenames with numbers."""
    numbers = [int(s) for s in filename.split() if s.isdigit()]
    return numbers[0] if numbers else filename

def rename_files(folder_path):
    """Rename files in a folder and create a log and Excel file."""
    log_filename = "renamer.log"
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        filename=log_filename, 
                        filemode='a')

    # Check if the folder exists
    if not os.path.exists(folder_path):
        logging.error("The folder does not exist. Please check the path and try again.")
        print("The folder does not exist. Please check the path and try again.")
        return
    
    logging.info("Renaming and copying process started.")
    
    # List files in the folder
    files = os.listdir(folder_path)

    # Exit if no files are found
    if not files:
        logging.warning("No files found in the directory.")
        print("No files found in the directory.")
        return

    # Create a new folder for renamed files
    base_folder_path, original_folder_name = os.path.split(folder_path)
    new_folder_name = f"{original_folder_name}_renamed"
    new_folder_path = os.path.join(base_folder_path, new_folder_name)

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    # Generate random indices for renaming
    random_indices = random.sample(range(1, len(files) + 1), len(files))
    rename_data = []

    # Rename and copy files
    for filename, random_index in zip(files, random_indices):
        old_file = os.path.join(folder_path, filename)
        new_filename = f"file_{random_index}{os.path.splitext(filename)[1]}"
        new_file = os.path.join(new_folder_path, new_filename)

        shutil.copy(old_file, new_file)
        rename_data.append({'Old Filename': filename, 'New Filename': new_filename})

        logging.info(f"Copied and renamed {filename} to {new_filename}")
        print(f"Copied and renamed {filename} to {new_filename}")

    # Create a DataFrame with renaming information
    df = pd.DataFrame(rename_data)

    # Write DataFrame to an Excel file
    if not df.empty:
        excel_filename = os.path.join(new_folder_path, 'rename_log.xlsx')
        with pd.ExcelWriter(excel_filename) as writer:
            df.sort_values(by='Old Filename', key=lambda x: x.map(sort_key)).to_excel(writer, index=False, sheet_name='Sorted by Original Name')
            df.sort_values(by='New Filename').to_excel(writer, index=False, sheet_name='Sorted by New Name')

        logging.info(f"Renaming and copying complete. Log saved to {excel_filename}.")
        print(f"Renaming and copying complete. Log saved to {excel_filename}.")
    else:
        logging.error("DataFrame is empty. No data to write to Excel.")
        print("DataFrame is empty. No data to write to Excel.")
