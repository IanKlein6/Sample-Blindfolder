import tkinter as tk
import os
from tkinter import filedialog, messagebox, simpledialog
import threading
from renamer import process_folders  # Assume process_folders in renamer.py handles all logic

class FolderSelector:
    def __init__(self, root):
        self.root = root
        self.folders = []

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
        folder_path = filedialog.askdirectory()
        if folder_path and folder_path not in self.folders:
            self.folders.append(folder_path)
            self.update_folder_list()

    def remove_folder(self, folder):
        if folder in self.folders:
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
        
        base_output_folder = filedialog.askdirectory(title="Select a destination folder for the renamed files")
        if not base_output_folder:
            return
        
        output_folder_name = simpledialog.askstring("Output Folder", "Enter a name for the new folder:")
        if not output_folder_name:
            messagebox.showwarning("Warning", "No folder name provided.")
            return

        output_folder = os.path.join(base_output_folder, output_folder_name)
        if os.path.exists(output_folder):
            messagebox.showwarning("Warning", f"The folder {output_folder_name} already exists.")
            return
        
        os.makedirs(output_folder)

        # Run the process in a separate thread
        process_thread = threading.Thread(target=process_folders, args=(self.folders, output_folder), daemon=True)
        process_thread.start()

# Create the main window
root = tk.Tk()
app = FolderSelector(root)
root.mainloop()
