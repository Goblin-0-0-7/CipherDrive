import logging
import cv2
import Hellpers as hell

def decrypt_frame(frame, data_width, data_height, pix_size, compression_err):
    logger = logging.getLogger("CipherDrive")

    binary = ""
    empty_pixel = 0
    for y in range(0, data_height):
        for x in range(0, data_width):
            #pixel = frame.getpixel((x*pix_size,y*pix_size)) #using Image from PIL
            pixel = frame[y*pix_size, x*pix_size] #using openCV

            #reading max/min of the rgb values in case of black and white frames
            if min(pixel) <= 0 + compression_err: #convention is black == 1, white == 0
                binary += "1"
            elif max(pixel) >= 255 - compression_err:
                binary += "0"
            else:
                empty_pixel +=1
    logger.into("{} pixel had no data or where not identifed as black or white".format(empty_pixel))
    return binary

def decrypt_first_frame(frame, width, compression_err):
    logger = logging.getLogger("CipherDrive")

    binary = ""
    empty_pixel = 0
    pix_size = int(width / 32)
    for y in range(0, 18):
        for x in range(0, 32):
            pixel = frame[y*pix_size, x*pix_size] #using openCV

            #reading max/min of the rgb values in case of black and white frames
            if min(pixel) <= 0 + compression_err: #convention is black == 1, white == 0
                binary += "1"
            elif max(pixel) >= 255 - compression_err:
                binary += "0"
            else:
                empty_pixel +=1
    logger.info("{} pixel had no data or where not identifed as black or white".format(empty_pixel))

    indices = [0,8,12,62]
    b_fps, b_pix_size, b_file_extension, b_file_name = [binary[i:j] for i,j in zip(indices, indices[1:]+[None])]
    fps = int(b_fps, 2)
    pix_size = int(b_pix_size, 2)
    file_extension = hell.int2strABC(hell.binary2intsABC(b_file_extension))
    file_name = hell.binary2str(b_file_name)
    return fps, pix_size, file_extension, file_name

def decrypt_video(video_dir: str, compression_err):

    cap = cv2.VideoCapture(video_dir)

    if cap.isOpened():
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    data = ""
    first_frame = True
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if first_frame:
                fps, pix_size, file_extension, file_name = decrypt_first_frame(frame, width, compression_err)
                data_width = int(width/pix_size)
                data_height = int(height/pix_size)
                first_frame = False
            else:
                data += decrypt_frame(frame, data_width, data_height, pix_size, compression_err)
        else:
            break


    byte_data = int(data, 2).to_bytes((len(data) + 7) // 8, byteorder='big')
    return byte_data, file_extension, file_name
