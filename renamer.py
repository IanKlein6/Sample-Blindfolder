import os
import random
import logging
import pandas as pd
import shutil

def sort_key(filename):
    """Custom sorting key to sort filenames with numbers."""
    numbers = [int(s) for s in filename.split() if s.isdigit()]
    return numbers[0] if numbers else filename

def process_folders(folders, destination_folder):
    """Process multiple folders and rename files in batches."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Copy all files from selected folders to the destination folder
    for folder in folders:
        for file_name in os.listdir(folder):
            source = os.path.join(folder, file_name)
            if os.path.isfile(source):
                destination = os.path.join(destination_folder, file_name)
                shutil.copy(source, destination)

    # Now, call rename_files on the destination folder
    rename_files(destination_folder)

def rename_files(folder_path, batch_size=50):
    """Rename files in a folder in batches and create a log and Excel file."""
    log_filename = "renamer.log"

    # Configure logging
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        filename=log_filename, 
                        filemode='a')

    if not os.path.exists(folder_path):
        logging.error("The folder does not exist. Please check the path and try again.")
        return

    logging.info("Renaming process started.")
    
    all_files = sorted(os.listdir(folder_path), key=sort_key)
    if not all_files:
        logging.warning("No files found in the directory.")
        return

    total_files = len(all_files)
    rename_data = []
    index_offset = 1

    # Process files in batches
    for batch_start in range(0, total_files, batch_size):
        batch_files = all_files[batch_start:batch_start + batch_size]
        indices = random.sample(range(index_offset, index_offset + len(batch_files)), len(batch_files))

        for filename, index in zip(batch_files, indices):
            old_file = os.path.join(folder_path, filename)
            new_filename = f"image_{index}{os.path.splitext(filename)[1]}"
            new_file = os.path.join(folder_path, new_filename)
            
            os.rename(old_file, new_file)
            rename_data.append({'Old Filename': filename, 'New Filename': new_filename})

            logging.info(f"Renamed {filename} to {new_filename}")

        index_offset += len(batch_files)

    # Generate Excel log after all batches are processed
    if rename_data:
        df = pd.DataFrame(rename_data)
        excel_filename = os.path.join(folder_path, 'rename_log.xlsx')
        with pd.ExcelWriter(excel_filename) as writer:
            df.sort_values(by='Old Filename', key=lambda x: x.map(sort_key)).to_excel(writer, index=False, sheet_name='Sorted by Original Name')
            df.sort_values(by='New Filename').to_excel(writer, index=False, sheet_name='Sorted by New Name')

        logging.info(f"Renaming process complete. Log saved to {excel_filename}.")
    else:
        logging.error("DataFrame is empty. No data to write to Excel.")
