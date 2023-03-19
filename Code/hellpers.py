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
def char2intABC(s: str):
    return ord(s.lower()) - 96 #number between 0-25

def int2charABC(i: int):
    if i == 0:
        return ""
    else:
        return chr(i + 96)

def str2intABC(sss: str):
    iii = []
    for s in sss:
        iii.append(char2intABC(s))
    return iii

def int2strABC(iii: list):
    sss = ""
    for i in iii:
        sss += int2charABC(i)
    return sss

def ints2binaryABC(iii: list):
    binary = ""
    for i in iii:
        bits = "{:05b}".format(i)
        binary += str(bits)
    return binary

def binary2intsABC(binary: str):
    iii = []
    for bin in [binary[i:i+5] for i in range(0, len(binary), 5)]:
        bin = bin.zfill(8)
        iii.append(int(bin, 2))
    return iii

def binary2str(binary: str):
    sss = ""
    for bin in [binary[i:i+8] for i in range(0, len(binary), 8)]:
        sss += chr(int(bin, 2))
    return sss