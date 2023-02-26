from PIL import Image

class Converter:

    def __init__(self, width, height, pix_size):
        self.width = width
        self.height = height
        self.pix_size = pix_size

    def standby(self):
        self.standby = True

    def run(self, chunk, chunk_index):
        frame = Image.new('1', (self.width, self.height), color='white') #create new white frame

        for y in range(0, int(self.height/self.pix_size)):
            for x in range(0, int(self.width/self.pix_size)):
                binary_index = y*int(self.width/self.pix_size) + x
                if binary_index < len(chunk):
                    for i in range(self.pix_size*x, self.pix_size*x+self.pix_size):
                        for k in range(self.pix_size*y, self.pix_size*y+self.pix_size):
                            frame.putpixel((i,k), int(chunk[binary_index]))

        frame.save("frame{}.png".format(chunk_index))
