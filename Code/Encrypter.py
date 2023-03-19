from PIL import Image

class Encrypter:

    def __init__(self, folder_dir, width, height, pix_size, index, first_frame: bool = False):
        self.width = width
        self.height = height
        self.pix_size = pix_size
        self.index = index
        self.folder_dir = folder_dir
        self.first_frame = first_frame

    def standby(self): #useless?
        self.standby = True

    def run(self, chunk, chunk_index):
        frame = Image.new('L', (self.width, self.height), color=128) #create new gray frame ("L" means grayscale mode)

        data_width = int(self.width/self.pix_size)
        data_height = int(self.height/self.pix_size)

        if self.first_frame:
            binary_index = 0
            for y in range(0, data_height):
                for x in range(0, data_width):
                    if (y == 0 and binary_index < 8) or (y == 1 and binary_index < 12) or ((y == 2 or y == 3) and binary_index < 62) or (y >= 4 and binary_index < len(chunk)):
                        """ structure:
                        8 pixel -> fps
                        4 pixel -> pixel size
                        32 pixel -> file extension (I)
                        18 pixel -> file extension (II)
                        rest -> file name
                        """
                        for i in range(self.pix_size*y, self.pix_size*y + self.pix_size):
                            for k in range(self.pix_size*x, self.pix_size*x + self.pix_size):
                                if int(chunk[binary_index]) == 1: #1 == black, white == 0                           
                                    frame.putpixel((k,i), 0)
                                else:
                                    frame.putpixel((k,i), 255)                 
                    else:
                        break
                    binary_index += 1

            frame.save(self.folder_dir + "/first_frame.png")
        else:
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
