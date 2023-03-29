
def generate_file(byte_data, file_name: str, extension):
    with open('{}.{}'.format(file_name, extension), 'wb') as f:
        f.write(byte_data)