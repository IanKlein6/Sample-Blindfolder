import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from renamer import rename_files  # Import the function from your script

def select_folder():
    """Callback function to select a folder and perform file renaming."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        try:
            rename_files(folder_path)
            messagebox.showinfo("Success", "Files renamed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("File Renamer")

# Add instructions label
instructions_label = tk.Label(root, text="Click the button below to select a folder for file renaming.")
instructions_label.pack(pady=(20, 10))  # Add extra vertical padding between label and button

# Create a standard button to select folder
select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.pack(pady=(0, 20))  # Add extra vertical padding between button and window edge

# Center the button horizontally and vertically
root.update_idletasks()  # Update the window to calculate button size
button_width = select_button.winfo_width()
button_height = select_button.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - button_width) // 2
y_position = (screen_height - button_height) // 2
root.geometry(f"+{x_position}+{y_position}")

# Start the GUI event loop
root.mainloop()
