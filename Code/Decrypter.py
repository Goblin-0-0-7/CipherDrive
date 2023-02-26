from PIL import Image

frame = Image.open("frame0.png")

width = 1280
height = 720

binary_lenght = 18 * 8
pix_size = 2

binary = ""

data_width = int(width/pix_size)
data_height = int(height/pix_size)

binary_index = 0
for y in range(0, data_height):
    for x in range(0, data_width):
        if binary_index < binary_lenght:
            pixel = frame.getpixel((x*pix_size,y*pix_size))
            if pixel == 0: #convention is black == 0, white == 1
                binary += "0"
            elif pixel == 255:
                binary += "1"
            else:
                print("This ({}) is not a black or white pixel".format(pixel))
                quit()
        else:
            break
        binary_index += 1
print(binary_index)
print(binary)

for i in range(0, len(binary), 8):
    print (chr(int(binary[i:i+8], 2)))
        