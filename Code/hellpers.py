import sys
import os

def create_folder(folder_name, folder_dir=None, next_to_file:bool =True):
    if next_to_file:
        # Get the directory where the script or executable is located
        if getattr(sys, 'frozen', False):
            # If the script is run as a standalone executable
            dir = os.path.dirname(sys.executable)
        else:
            # If the script is run as a Python file
            dir = os.path.dirname(os.path.abspath(__file__))

        # Create a new folder called "new_folder" in the same directory as the script or executable
        folder_dir = os.path.join(dir, folder_name)
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        return folder_dir
    else:
        print("TODO: add create folder in directory to hellpers.create_folder")

def count_files(folder_dir):
    return len([name for name in os.listdir(folder_dir) if os.path.isfile(folder_dir + "/" + name)])