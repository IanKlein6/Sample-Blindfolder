import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import threading
import os
import shutil
import logging
import pandas as pd

# Backend processing
def sort_key_old(filename):
    numbers = [int(s) for s in filename.split() if s.isdigit()]
    return numbers[0] if numbers else filename.lower()

def sort_key_new(filename):
    try:
        return int(filename.split('_')[1].split('.')[0])
    except (IndexError, ValueError):
        return 0


def process_folders(folders, destination_folder):
    # Configure logging to output to the console
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    logging.info("Process started.")

    rename_data = []
    index = 1

    for folder in folders:
        for file_name in sorted(os.listdir(folder), key=sort_key_old):
            source = os.path.join(folder, file_name)
            if os.path.isfile(source):
                new_filename = f"image_{index}{os.path.splitext(file_name)[1]}"
                destination = os.path.join(destination_folder, new_filename)
                
                shutil.copy(source, destination)
                rename_data.append({'Old Filename': file_name, 'New Filename': new_filename})
                logging.info(f"File from {source} renamed to {new_filename} in {destination_folder}")

                index += 1

    if rename_data:
        df = pd.DataFrame(rename_data)
        excel_filename = os.path.join(destination_folder, 'rename_log.xlsx')
        with pd.ExcelWriter(excel_filename) as writer:
            df.sort_values(by='Old Filename', key=lambda x: x.map(sort_key_old)).to_excel(writer, index=False, sheet_name='Sorted by Original Name')
            df.sort_values(by='New Filename', key=lambda x: x.map(sort_key_new)).to_excel(writer, index=False, sheet_name='Sorted by New Name')



# GUI
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

        # Move the folder creation and file processing to a separate thread
        threading.Thread(target=lambda: process_folders(self.folders, output_folder), daemon=True).start()

# Create the main window
root = tk.Tk()
app = FolderSelector(root)
root.mainloop()
