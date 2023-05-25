import cv2
import os
import math
from threading import Thread
from Encrypter import Encrypter
import Hellpers as hell

def rip_bytes(path: str):
    file = open(path, "rb") #opening for [r]eading as [b]inary
    byte_data = file.read()
    file.close()
    if not byte_data: return "File is empty"
    return byte_data

def rip_binary(byte_data):
    binary_data = ""
    for byte in byte_data:
        bits = "{:08b}".format(byte)
        binary_data += str(bits)
    return binary_data

def stich(binary, file_name, width, height, pix_size, threads, save_dir, callback):
    
    folder_dir = hell.create_dir(save_dir + "/" + file_name)
    length = len(binary)

    frame_size = (width * height)
    frame_data_size = frame_size / pow(pix_size, 2)
    frame_length = math.ceil(length / frame_data_size)
    chunk_frame_size = math.ceil(frame_length / threads)
    chunk_data_size = int(chunk_frame_size * frame_data_size)

    chunks = [binary[i:i+chunk_data_size] for i in range(0, length, chunk_data_size)] #seperates binary into equal chunks
    
    def finished_frame(thread, frame):
        callback(thread, frame, frame_length)

    encrypters = []
    encrypter_threads = []
    for index in range(len(chunks)):
        new_encrypter = Encrypter(folder_dir, width, height, pix_size, index)
        encrypters.append(new_encrypter)
        new_encrypter_thread = Thread(target= new_encrypter.run, args=(chunks[index], finished_frame, ))
        encrypter_threads.append(new_encrypter_thread)

    for thread in encrypter_threads:
        thread.start()
    
    for thread in encrypter_threads: #wait for threads to finish
        thread.join()

    return folder_dir


def unite(image_folder, fps, threads):
    file_name = os.path.basename(image_folder)
    video_name = file_name + ".avi"

    frames = []
    frames.append("first_frame.png")
    frames_length = hell.count_files(image_folder)
    for th_index in range(threads):
        for f_index in range(frames_length):
            for img in os.listdir(image_folder):
                if img.startswith("thread{}_frame{}".format(th_index, f_index)):
                    frames.append(img)
    control_frame = cv2.imread(image_folder + "/" + frames[0])
    height, width, channels = control_frame.shape
    video = cv2.VideoWriter(image_folder + "/" + video_name, 0, fps, (width,height)) #saving as avi

    for frame in frames:
        video.write(cv2.imread(os.path.join(image_folder, frame)))

    cv2.destroyAllWindows()
    video.release()

def create_first_frame(file_name: str, width: int, height: int, pix_size: int, fps: int, extension: str, frames_dir: str):
    b_file_name = rip_binary(file_name.encode('ascii', 'replace'))
    b_extension = hell.ints2binaryABC(hell.str2intABC(extension)).ljust(50, "0") #saved in 50 bits (5 bits per char)
    b_pix_size = "{:04b}".format(pix_size, 'b') #saved in 4 bits
    b_fps = "{:08b}".format(fps, 'b') #saved in 8 bits
    b_first_frame_data = b_fps + b_pix_size + b_extension + b_file_name

    first_frame_pix_size = int(width / 32)

    encrypter = Encrypter(frames_dir, width, height, first_frame_pix_size, -1, True)
    encrypter.run(b_first_frame_data)