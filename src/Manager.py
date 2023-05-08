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
        global start_time
        start_time = t.time()
        file = os.path.basename(file_path)
        if file_name == "":
            file_name, extension = file.rsplit(".", 1)
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

        global finished_frames
        finished_frames = []
        frames_dir = rip.stich(binary, file_name, width, height, pix_size, threads, save_dir, self.stiched_frames_update)

        self.return_status(start_time, "stiched frames")

        rip.create_first_frame(file_name, width, height, pix_size, fps, extension, frames_dir)
        rip.unite(frames_dir, fps, threads)

        self.return_status(start_time, "video saved")
        self.callback("finished")
        return

    def decrypt(self, video_path, compression_err):
        byte_data, file_extension, file_name = dcr.decrypt_video(video_path, compression_err)
        video_dir = os.path.dirname(video_path)
        med.generate_file(byte_data, file_name, file_extension, video_dir)
        self.callback()
        return

    def stiched_frames_update(self, thread_index, frames_index, frames_length):
        finished_frames.append(f"thread{thread_index}_frame{frames_index}")
        completed_frames = len(finished_frames)
        msg = f"{completed_frames} / {frames_length} frames stiched"
        self.return_status(start_time, msg)

    def return_status(self, start_time, status: str):
        hours, min, sec = hell.delta_time(start_time)
        self.progress_info.setText(status + " {:02d}:{:02d}:{:02d}".format(hours, min, sec))
        self.logger.info(status + " {:02d}:{:02d}:{:02d}".format(hours, min, sec))
        """Terminal Version
        print(status + " {:02d}:{:02d}:{:02d}".format(hours, min, sec))
        """