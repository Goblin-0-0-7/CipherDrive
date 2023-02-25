
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



bytes = rip_bytes("YoutubeDataSaverTestFile.txt")
binary = (rip_binary(bytes))

for i in range(0, len(binary), 8):
    print (chr(int(binary[i:i+8], 2)))