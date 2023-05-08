import logging
from logging.handlers import RotatingFileHandler
import datetime
import Hellpers as hell

def create_logger():
    log_dir = hell.create_dir("log/", next_to_file=True)
    log_filename = log_dir + 'CipherDrive' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
    handler = RotatingFileHandler(log_filename, maxBytes= 1024 * 1024 * 10, backupCount=5) #10 MB
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger = logging.getLogger("CipherDrive")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    delete_old_logs(log_dir, max_logs=5)

def delete_old_logs(log_dir: str, max_logs: int = 5):
    if hell.count_files(log_dir) > max_logs:
        hell.delete_oldest(log_dir)
