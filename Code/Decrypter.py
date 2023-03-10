from PIL import Image
import cv2

def decrypt_img(frame, data_width, data_height, pix_size, compression_err):
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
    print("{} pixel had no data or where not identifed as black or white".format(empty_pixel))
    return binary

def decrypt_video(video_dir: str, width, height, pix_size, compression_err):

    data_width = int(width/pix_size)
    data_height = int(height/pix_size)

    cap = cv2.VideoCapture(video_dir)

    data = ""
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            data += decrypt_img(frame, data_width, data_height, pix_size, compression_err)
        else:
            break


    byte_data = int(data, 2).to_bytes((len(data) + 7) // 8, byteorder='big')
    return byte_data
