import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import threading
import datetime
import random
import os
import shutil
import logging
import pandas as pd
import re

# Extract numbers from filenames for sorting
def extract_number_for_sorting(filename):
    numbers = re.findall(r'\d+', filename)
    return tuple(int(num) for num in numbers)

# Process folders, rename files, and create an Excel log
def process_folders(folders, destination_folder):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    logging.info("Process started.")

    all_files = []
    for folder in folders:
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            if os.path.isfile(file_path):
                all_files.append(file_path)

    random.shuffle(all_files)
    current_date = datetime.datetime.now().strftime("%y%m%d")
    rename_data = []

    for index, file_path in enumerate(all_files, start=1):
        file_name = os.path.basename(file_path)
        new_filename = f"{current_date}_sample_{index}{os.path.splitext(file_name)[1]}"
        destination_path = os.path.join(destination_folder, new_filename)
        
        shutil.copy(file_path, destination_path)
        rename_data.append({'Old Filename': file_name, 'New Filename': new_filename})

    if rename_data:
        df = pd.DataFrame(rename_data)
        excel_filename = os.path.join(destination_folder, 'rename_log.xlsx')
        with pd.ExcelWriter(excel_filename) as writer:
            sorted_new = df.sort_values(by='New Filename', key=lambda x: x.map(extract_number_for_sorting))
            sorted_new[['New Filename', 'Old Filename']].to_excel(writer, index=False, sheet_name='Sorted by New Name')

            sorted_old = df.sort_values(by='Old Filename', key=lambda x: x.map(extract_number_for_sorting))
            sorted_old[['Old Filename', 'New Filename']].to_excel(writer, index=False, sheet_name='Sorted by Original Name')

        logging.info(f"Renaming process complete. Log saved to {excel_filename}.")
    else:
        logging.error("No files processed.")

# GUI for folder selection and file processing
class FolderSelector:
    def __init__(self, root):
        self.root = root
        self.folders = []
        self.last_dir = os.path.expanduser("~")

        self.root.title("File Renamer")
        self.instructions_label = tk.Label(self.root, text="Add folders for file renaming and click 'Rename Files' when ready.")
        self.instructions_label.pack(pady=(20, 10))

        self.folder_frame = tk.Frame(self.root)
        self.folder_frame.pack(pady=(5, 20))

        self.add_folder_button = tk.Button(self.root, text="Add Folder", command=self.add_folder)
        self.add_folder_button.pack(side=tk.LEFT, padx=(20, 10))

        self.rename_button = tk.Button(self.root, text="Rename Files", command=self.start_renaming_process)
        self.rename_button.pack(side=tk.RIGHT, padx=(10, 20))

    def add_folder(self):
        folder_path = filedialog.askdirectory(initialdir=self.last_dir)
        if folder_path:
            self.last_dir = os.path.dirname(folder_path)
            if folder_path not in self.folders:
                self.folders.append(folder_path)
                self.update_folder_list()

    def remove_folder(self, folder):
        self.folders.remove(folder)
        self.update_folder_list()

    def update_folder_list(self):
        for widget in self.folder_frame.winfo_children():
            widget.destroy()
        for folder in self.folders:
            folder_frame = tk.Frame(self.folder_frame)
            folder_frame.pack(fill=tk.X)
            folder_label = tk.Label(folder_frame, text=folder)
            folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            remove_button = tk.Button(folder_frame, text="-", command=lambda f=folder: self.remove_folder(f))
            remove_button.pack(side=tk.RIGHT)

    def start_renaming_process(self):
        if not self.folders:
            messagebox.showwarning("Warning", "No folders selected.")
            return
        base_output_folder = filedialog.askdirectory(initialdir=self.last_dir, title="Select a destination folder for the renamed files")
        if not base_output_folder:
            return
        self.last_dir = os.path.dirname(base_output_folder)
        output_folder_name = simpledialog.askstring("Output Folder", "Enter a name for the new folder:")
        if not output_folder_name:
            return
        output_folder = os.path.join(base_output_folder, output_folder_name)
        if os.path.exists(output_folder):
            messagebox.showwarning("Warning", f"The folder {output_folder_name} already exists.")
            return
        threading.Thread(target=lambda: process_folders(self.folders, output_folder), daemon=True).start()

# Run the GUI
root = tk.Tk()
app = FolderSelector(root)
root.mainloop()
