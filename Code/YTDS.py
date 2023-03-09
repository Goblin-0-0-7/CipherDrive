import cv2
import os
import sys
import math
from threading import Thread
from Encrypter import Encrypter

#default settings
width = 1280
height = 720
pix_size = 2
fps = 1
threads = 8
file = "Cube.jpg"

file_name = file.split(".")[0]

# Get the directory where the script or executable is located
if getattr(sys, 'frozen', False):
    # If the script is run as a standalone executable
    dir = os.path.dirname(sys.executable)
else:
    # If the script is run as a Python file
    dir = os.path.dirname(os.path.abspath(__file__))

# Create a new folder called "new_folder" in the same directory as the script or executable
folder_dir = os.path.join(dir, file_name)
if not os.path.exists(folder_dir):
    os.makedirs(folder_dir)



def rip_bytes(path: str):
    file = open(path, "rb") #opening for [r]eading as [b]inary
    byte_data = file.read()
    file.close()
    if not byte_data: print("File is empty")
    print("Byte length: {}".format(len(byte_data)))
    return byte_data

def rip_binary(byte_data):
    binary_data = ""
    for byte in byte_data:
        bits = "{:08b}".format(byte)
        binary_data += str(bits)
    return binary_data

def stich(binary):
    length = len(binary)

    frame_size = (width * height)
    frame_data_size = frame_size / pow(pix_size, 2)
    frame_length = math.ceil(length / frame_data_size)
    chunk_frame_size = math.ceil(frame_length / threads)
    chunk_data_size = int(chunk_frame_size * frame_data_size)

    chunks = [binary[i:i+chunk_data_size] for i in range(0, len(binary), chunk_data_size)] #seperates binary into equal chunks
    
    encrypters = []
    encrypter_threads = []
    for index in range(threads):
        new_encrypter = Encrypter(folder_dir, width, height, pix_size, index)
        encrypters.append(new_encrypter)
        new_encrypter_thread = Thread(target= new_encrypter.standby, args=( ))
        new_encrypter_thread.start()
        encrypter_threads.append(new_encrypter_thread)

    for index in range(len(chunks)):
        encrypters[index].run(chunks[index], index)

def unite():
    image_folder = folder_dir
    video_name = file_name + ".avi"

    frames = []
    for index in range(threads):
        for img in os.listdir(image_folder):
            if img.startswith("thread{}".format(index)):
                frames.append(img)         
    
    video = cv2.VideoWriter(video_name, 0, fps, (width,height)) #saving as avi

    for frame in frames:
        video.write(cv2.imread(os.path.join(image_folder, frame)))

    cv2.destroyAllWindows()
    video.release()

bytes = rip_bytes(file)
binary = (rip_binary(bytes))
stich(binary)
unite()


#debug
print(binary)


