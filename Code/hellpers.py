import sys
import os
import time as t

#dir hellpers
def create_folder(folder_name, folder_dir=None, next_to_file: bool =True):
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

#time hellpers
def delta_time(start_time):
    t_sec = round(t.time() - start_time)
    (t_min, t_sec) = divmod(t_sec,60)
    (t_hour,t_min) = divmod(t_min,60)
    return t_hour, t_min, t_sec

#converter
def char2int(s: str):
    return ord(s.lower()) - 97 #number between 0-25

def int2char(i: int):
    return chr(i + 97)

def str2int(sss: str):
    iii = []
    for s in sss:
        iii.append(char2int(s))
    return iii

def int2str(iii: list):
    sss = ""
    for i in iii:
        sss += int2char(i)
    return sss

def ints2binary(iii: list):
    binary = ""
    for i in iii:
        bits = "{:05b}".format(i)
        binary += str(bits)
    return binary

def binary2ints(binary: str):
    iii = []
    for bin in [binary[i:i+5] for i in range(0, len(binary), 5)]:
        bin = bin.zfill(8)
        iii.append(int(bin, 2))
    return iii