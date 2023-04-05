import os
import time as t
import logging
import Ripper as rip
import Decrypter as dcr
import Medic as med
import Hellpers as hell

class Manager:

    def __init__(self, progress_info, callback):
        self.progress_info = progress_info
        self.callback = callback
        self.logger = logging.getLogger("CipherDrive")

    def encrypt(self, file_path: str, save_dir: str ,width: int, height: int, pix_size: int = 2, fps: int = 1, threads: int = 8, file_name: str = ""):
        start_time = t.time()
        file = os.path.basename(file_path)
        if file_name == "":
            file_name, extension = file.split(".")
        else:
            extension = file.split(".")[1]
        bytes = rip.rip_bytes(file_path)
        if bytes == "File is empty":
            self.callback("file empty")
            return
        self.logger.info(f"Byte length: {len(bytes)}")

        self.return_status(start_time, "ripped bytes")

        binary = rip.rip_binary(bytes)

        self.return_status(start_time, "ripped binary")

        frames_dir = rip.stich(binary, file_name, width, height, pix_size, threads, save_dir)

        self.return_status(start_time, "stiched frames")

        rip.create_first_frame(file_name, width, height, pix_size, fps, extension, frames_dir)
        rip.unite(frames_dir, fps, threads)

        self.return_status(start_time, "video saved")
        self.callback("finished")
        return

    def decrypt(self, video_dir, compression_err):
        byte_data, file_extension, file_name = dcr.decrypt_video(video_dir, compression_err)
        med.generate_file(byte_data, file_name, file_extension, video_dir)
        self.callback()
        return

    def return_status(self, start_time, status: str):
        hours, min, sec = hell.delta_time(start_time)
        self.progress_info.setText(status + " {:02d}:{:02d}:{:02d}".format(hours, min, sec))
        self.logger.info(status + " {:02d}:{:02d}:{:02d}".format(hours, min, sec))
        """Terminal Version
        print(status + " {:02d}:{:02d}:{:02d}".format(hours, min, sec))
        """