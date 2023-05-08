
def generate_file(byte_data, file_name: str, extension, save_dir):
    with open(save_dir + "/" + '{}.{}'.format(file_name, extension), 'wb') as file:
        file.write(byte_data)