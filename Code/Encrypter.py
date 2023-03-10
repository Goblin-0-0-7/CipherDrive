from PIL import Image

class Encrypter:

    def __init__(self, folder_dir, width, height, pix_size, index):
        self.width = width
        self.height = height
        self.pix_size = pix_size
        self.index = index
        self.folder_dir = folder_dir

    def standby(self):
        self.standby = True

    def run(self, chunk, chunk_index):
        frame = Image.new('L', (self.width, self.height), color=128) #create new gray frame ("L" means grayscale mode)

        data_width = int(self.width/self.pix_size)
        data_height = int(self.height/self.pix_size)

        binary_index = 0
        for y in range(0, data_height):
            for x in range(0, data_width):

                if binary_index < len(chunk):
                    for i in range(self.pix_size*y, self.pix_size*y + self.pix_size):
                        for k in range(self.pix_size*x, self.pix_size*x + self.pix_size):
                            if int(chunk[binary_index]) == 1: #1 == black, white == 0                           
                                frame.putpixel((k,i), 0)
                            else:
                                frame.putpixel((k,i), 255)
                else:
                    break
                binary_index += 1

        frame.save(self.folder_dir + "/thread{}_frame{}.png".format(self.index, chunk_index))
