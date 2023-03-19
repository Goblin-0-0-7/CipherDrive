import time as t
import Ripper as rip
import Decrypter as dcr
import Medic as med
import Hellpers as hell

compression_err = 30 #setting for decrypt missing, in 1 frame?
video_dir = "triumph.avi"
dcr_file_name = "test1"

file = "triumph.txt"
#file = "triumph.txt"

job = "decrypt" # encrypt and decrpyt

#default settings for encrypt
width = 1280
height = 720
pix_size = 2
fps = 1
threads = 8
file_name, extension = file.split(".")


if job == "encrypt":

    start_time = t.time()

    bytes = rip.rip_bytes(file)

    hours, min, sec = hell.delta_time(start_time)
    print("ripped bytes {:02d}:{:02d}:{:02d}".format(hours, min, sec))

    binary = rip.rip_binary(bytes)

    hours, min, sec = hell.delta_time(start_time)
    print("ripped binary {:02d}:{:02d}:{:02d}".format(hours, min, sec))

    frames_dir = rip.stich(binary, file_name, width, height, pix_size, threads)

    hours, min, sec = hell.delta_time(start_time)
    print("stiched frames {:02d}:{:02d}:{:02d}".format(hours, min, sec))

    rip.create_first_frame(file_name, width, height, pix_size, fps, extension, frames_dir)

    rip.unite(frames_dir, fps, threads)

    hours, min, sec = hell.delta_time(start_time)
    print("united frames {:02d}:{:02d}:{:02d}".format(hours, min, sec))

elif job == "decrypt":
    byte_data, file_extension, file_name = dcr.decrypt_video(video_dir, width, height, pix_size, compression_err)
    med.generate_file(byte_data, file_name, file_extension)