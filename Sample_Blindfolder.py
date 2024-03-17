import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Toplevel, Label
import threading
import datetime
import random
import os
import shutil
import logging
import pandas as pd
import re

def extract_number_for_sorting(filename):
    numbers = re.findall(r'\d+', filename)
    return tuple(int(num) for num in numbers)

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
        rename_data.append({'Original Samples': file_name, 'Blind Samples': new_filename})

    if rename_data:
        df = pd.DataFrame(rename_data)
        excel_filename = os.path.join(destination_folder, 'Blindfold_log.xlsx')
        with pd.ExcelWriter(excel_filename) as writer:
            sorted_new = df.sort_values(by='Blind Samples', key=lambda x: x.map(extract_number_for_sorting))
            sorted_new[['Blind Samples', 'Original Samples']].to_excel(writer, index=False, sheet_name='Sorted by Blinded Samples')

            sorted_old = df.sort_values(by='Original Samples', key=lambda x: x.map(extract_number_for_sorting))
            sorted_old[['Original Samples', 'Blind Samples']].to_excel(writer, index=False, sheet_name='Sorted by Original Samples')

        logging.info(f"Renaming process complete. Log saved to {excel_filename}.")

class FolderSelector:
    def __init__(self, root):
        self.root = root
        self.folders = []
        self.last_dir = os.path.expanduser("~")

        self.root.title("Sample Blindfolder")
        self.instructions_label = tk.Label(self.root, text="Add folders for Sample Blindfolding and click 'Destination - Blindfold' when ready.")
        self.instructions_label.pack(pady=(20, 10))

        self.folder_frame = tk.Frame(self.root)
        self.folder_frame.pack(pady=(5, 20))

        self.add_folder_button = tk.Button(self.root, text="Add Folder", command=self.add_folder)
        self.add_folder_button.pack(side=tk.LEFT, padx=(20, 10))

        self.rename_button = tk.Button(self.root, text="Destination - Blindfold", command=self.start_renaming_process)
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

        base_output_folder = filedialog.askdirectory(initialdir=self.last_dir, title="Select a destination folder for the Blindfolded files")
        if not base_output_folder:
            return

        self.last_dir = os.path.dirname(base_output_folder)
        output_folder_name = simpledialog.askstring("Output Folder", "Enter a name for the new folder:", parent=self.root)
        if not output_folder_name:
            return

        output_folder = os.path.join(base_output_folder, output_folder_name)
        if os.path.exists(output_folder):
            messagebox.showwarning("Warning", f"The folder {output_folder_name} already exists.")
            return

        # Start the processing after confirmation
        self.initiate_processing(output_folder)
    
    def rename_files_thread(self, folders, destination_folder):
        try:
            process_folders(folders, destination_folder)
        except Exception as e:
            print(f"Error processing folders: {e}")
        finally:
            self.processing_complete = True
            # Schedule the completion message to be shown in the main thread
            self.root.after(100, self.check_process_completion)

    def initiate_processing(self, output_folder):
        self.output_folder = output_folder
        self.loading_window = Toplevel(self.root)
        self.loading_window.title("Processing")
        Label(self.loading_window, text="Processing... Please wait").pack(padx=20, pady=20)

        # Start the renaming process in a separate thread
        self.processing_complete = False
        thread = threading.Thread(target=lambda: self.rename_files_thread(self.folders, output_folder), daemon=True)
        thread.start()


    def check_process_completion(self):
        if self.processing_complete:
            self.loading_window.destroy()
            self.show_completion_message()
        else:
            self.root.after(100, self.check_process_completion)

    def show_completion_message(self):
        # Create a top-level window to show the completion message
        self.completion_window = Toplevel(self.root)
        self.completion_window.title("Completed")
        Label(self.completion_window, text="Files have been successfully Blindfolded and Logged.").pack(padx=20, pady=20)
        
        # Button to open the destination folder
        open_button = tk.Button(self.completion_window, text="Open Folder", command=self.open_destination_folder)
        open_button.pack(pady=10)

    def open_destination_folder(self):
        try:
            if os.name == 'nt': # Windows
                os.startfile(self.output_folder)
            elif os.name == 'posix': # macOS and Linux
                if os.uname().sysname == 'Darwin': # macOS
                    os.system(f'open "{self.output_folder}"')
                else: # Linux
                    os.system(f'xdg-open "{self.output_folder}"')
        except Exception as e:
            print(f"Failed to open the folder: {e}")
            messagebox.showerror("Error", "Could not open the destination folder.")
        
        self.completion_window.destroy()




root = tk.Tk()
app = FolderSelector(root)
root.mainloop()
