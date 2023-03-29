import sys, os, glob
import time as t

#dir hellpers
def get_work_dir():
    # Get the directory where the script or executable is located
    if getattr(sys, 'frozen', False):
        # If the script is run as a standalone executable
        work_dir = os.path.dirname(sys.executable)
    else:
        # If the script is run as a Python file
        work_dir = os.path.dirname(os.path.abspath(__file__))
    return work_dir

def create_dir(dir, next_to_file: bool =False):
    if next_to_file:
        work_dir = get_work_dir()
        # Create a new folder called "new_folder" in the same directory as the script or executable
        folder_dir = os.path.join(work_dir, dir)
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        return folder_dir
    else:
        if not os.path.exists(dir):
            os.makedirs(dir)

def count_files(folder_dir):
    return len([name for name in os.listdir(folder_dir) if os.path.isfile(folder_dir + "/" + name)])

def delete_oldest(folder_dir):
    file_list = glob.glob(os.path.join(folder_dir, "*"))

    if not file_list:
        pass
    else:
        file_list.sort(key=lambda x: os.path.getctime(x))
        oldest_file = file_list[0]
        os.remove(oldest_file)

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