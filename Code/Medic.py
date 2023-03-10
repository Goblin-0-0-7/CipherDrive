
def generate_file(byte_data, file_name: str, extention):
    with open('{}.{}'.format(file_name, extention), 'wb') as f:
        f.write(byte_data)