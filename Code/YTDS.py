import math
from threading import Thread
from Encrypter import Encrypter

width = 1280
height = 720
pix_size = 2
threads = 8

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
        new_encrypter = Encrypter(width, height, pix_size)
        encrypters.append(new_encrypter)
        new_encrypter_thread = Thread(target= new_encrypter.standby, args=( ))
        new_encrypter_thread.start()
        encrypter_threads.append(new_encrypter_thread)

    for index in range(len(chunks)):
        encrypters[index].run(chunks[index], index)

bytes = rip_bytes("triumph.txt")
binary = (rip_binary(bytes))
stich(binary)

print(binary)

"""for i in range(0, len(binary), 8):
    print (chr(int(binary[i:i+8], 2)))"""