import cv2
import os
import sys
import math
from threading import Thread
from Encrypter import Encrypter
import Hellpers as hell

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

def stich(binary, file_name, width, height, pix_size, threads):
    folder_dir = hell.create_folder(file_name)
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

    return folder_dir

def unite(folder_dir, fps, threads):
    image_folder = folder_dir
    file_name = os.path.basename(folder_dir)
    video_name = file_name + ".avi"

    frames = []
    frames.append("first_frame.png")
    frames_length = hell.count_files(image_folder)
    for th_index in range(threads):
        for f_index in range(frames_length):
            for img in os.listdir(image_folder):
                if img.startswith("thread{}_frame{}".format(th_index, f_index)):
                    frames.append(img)
    control_frame = cv2.imread(os.path.join(image_folder, frames[0]))
    height, width, channels = control_frame.shape
    video = cv2.VideoWriter(video_name, 0, fps, (width,height)) #saving as avi

    for frame in frames:
        video.write(cv2.imread(os.path.join(image_folder, frame)))

    cv2.destroyAllWindows()
    video.release()

def create_first_frame(file_name: str, width: int, height: int, pix_size: int, fps: int, extension: str, frames_dir: str):
    b_file_name = rip_binary(file_name.encode('ascii', 'replace'))
    b_extension = hell.ints2binary(hell.str2int(extension)).ljust(50, "0") #saved in 50 bits (5 bits per char)
    b_pix_size = "{:04b}".format(pix_size, 'b') #saved in 4 bits
    b_fps = "{:08b}".format(fps, 'b') #saved in 8 bits
    b_first_frame_data = b_fps + b_pix_size + b_extension + b_file_name

    first_frame_pix_size = int(width / 32)

    encrypter = Encrypter(frames_dir, width, height, first_frame_pix_size, -1, True)
    encrypter_thread = Thread(target= encrypter.run, args=(b_first_frame_data, -1))
    encrypter_thread.start()