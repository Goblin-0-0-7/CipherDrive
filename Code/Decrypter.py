from PIL import Image
import cv2

#get those in first frame
width = 1280
height = 720
byte_length = 69515
binary_length = byte_length * 8
pix_size = 2
err = 30
video_dir = "Cube.avi"



data_width = int(width/pix_size)
data_height = int(height/pix_size)

def decrypt_img(frame):
    binary = ""
    binary_index = 0
    for y in range(0, data_height):
        for x in range(0, data_width):
            if binary_index < binary_length:
                #pixel = frame.getpixel((x*pix_size,y*pix_size)) #using  PIL Image
                pixel = frame[y*pix_size, x*pix_size] #using openCV

                #reading max/min of the rgb values in case of black and white frames
                if min(pixel) <= 0 + err: #convention is black == 0, white == 1
                    binary += "0"
                elif max(pixel) >= 255 - err:
                    binary += "1"
                else:
                    print("This ({}) is not a black or white pixel".format(pixel))
                    quit()
            else:
                break
            binary_index += 1
    print(binary_index)
    return binary

cap = cv2.VideoCapture(video_dir)

data = ""
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        data += decrypt_img(frame)
    else:
        break


byte_data = int(data, 2).to_bytes((len(data) + 7) // 8, byteorder='big')
print(byte_data)

with open('newfile.png', 'wb') as f:
    f.write(byte_data)

"""
for i in range(0, len(data), 8):
    print (chr(int(data[i:i+8], 2)))
"""