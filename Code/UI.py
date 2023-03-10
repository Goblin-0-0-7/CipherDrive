import time as t
import Ripper as rip


#default settings
width = 1280
height = 720
pix_size = 2
fps = 1
threads = 8
file = "Cube.jpg"

file_name = file.split(".")[0]

def delta_time(start_time):
    t_sec = round(t.time() - start_time)
    (t_min, t_sec) = divmod(t_sec,60)
    (t_hour,t_min) = divmod(t_min,60)
    return t_hour, t_min, t_sec

start_time = t.time()

bytes = rip.rip_bytes(file)

hours, min, sec = delta_time(start_time)
print("ripped bytes {:02d}:{:02d}:{:02d}".format(hours, min, sec))

binary = rip.rip_binary(bytes)

hours, min, sec = delta_time(start_time)
print("ripped binary {:02d}:{:02d}:{:02d}".format(hours, min, sec))

frames_dir = rip.stich(binary, file_name, width, height, pix_size, threads)

hours, min, sec = delta_time(start_time)
print("stiched frames {:02d}:{:02d}:{:02d}".format(hours, min, sec))

rip.unite(frames_dir, fps, threads)

hours, min, sec = delta_time(start_time)
print("united frames {:02d}:{:02d}:{:02d}".format(hours, min, sec))