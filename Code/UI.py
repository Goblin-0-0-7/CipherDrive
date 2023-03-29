import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi
from threading import Thread
import Bobbie as bob
import Hellpers as hell
import YTCS

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        bob.create_logger()
        loadUi("CipherDrive GUI.ui", self)
        self.toolButton_choose_dir.clicked.connect(self.choose_dir)
        self.pushButton_download.clicked.connect(self.start_download)
        self.lineEdit_url.textChanged.connect(self.check_url)

    def choose_dir(self):
        dir = QFileDialog.getExistingDirectory(self, "Choose Save Directory", hell.get_work_dir())
        self.lineEdit_save_dir.setText(dir)
    
    def download_finished(self, msg, start_time = 0, warnings = 0, errors = 0, not_deleted_files = 0):
        if msg == "finished":
            delta_time = time.time() - start_time
            delta_time_formated = time.strftime("%H:%M:%S", time.gmtime(delta_time))
            info_text = f"Download finished in: {delta_time_formated} with {warnings} warnings, {errors} errors"
            if not (not_deleted_files == 0):
                info_text += f"| {not_deleted_files} files could not be deleted"
        elif msg == "url error":
            info_text = "URL was not a downloadable source"
        elif msg == "video unavailable":
            info_text = "Video is regional unavailable"
        elif msg == "no access to playlist":
            info_text = "Can not access playlist. Check if playlist is set to private."
        self.label_download_info.setText(info_text)
        self.pushButton_download.setText("Start Download")
        self.pushButton_download.setEnabled(True)

    def start_download(self):
        url = self.lineEdit_url.text()
        dir = self.lineEdit_save_dir.text()
        video_flag = self.checkBox_video.isChecked()
        audio_flag = self.checkBox_audio.isChecked()
        url_type = YTCS.check_url(url)
        if self.radioButton_video.isChecked():
            flag = "video"
            first_video = 0
        elif self.radioButton_playlist.isChecked():
            flag = "playlist"
            if url_type == "playlist-video":
                url = "https://www.youtube.com/playlist?list=" + url.split("list=",1)[1].split("&index",1)[0] # takes the playlist id and appends it to a playlist link
            first_video = self.spinBox_first_entry.value()

        if url_type and dir and (video_flag or audio_flag):
            downloader = YTCS.Downloader(self.progressBar_video, self.label_download_info, self.download_finished)
            download_thread = Thread(target=downloader.download_url, args=(url, dir, video_flag, audio_flag, flag, first_video), daemon=True)
            download_thread.start()
            self.pushButton_download.setText("Downloading...")
            self.pushButton_download.setEnabled(False)

    def check_url(self):
        url = self.lineEdit_url.text()
        url_type = YTCS.check_url(url)
        if url_type == "playlist":
            self.radioButton_playlist.setEnabled(True)
            self.radioButton_video.setEnabled(False)
            self.uncheck_buttons()
            self.radioButton_playlist.setChecked(True)
            self.label_first_entry.setEnabled(True)
            self.spinBox_first_entry.setEnabled(True)
        elif url_type == "playlist-video":
            self.radioButton_playlist.setEnabled(True)
            self.radioButton_video.setEnabled(True)
            self.uncheck_buttons()
            self.label_first_entry.setEnabled(True)
            self.spinBox_first_entry.setEnabled(True)
        elif url_type == "video":
            self.radioButton_playlist.setEnabled(False)
            self.radioButton_video.setEnabled(True)
            self.uncheck_buttons()
            self.radioButton_video.setChecked(True)
            self.label_first_entry.setEnabled(False)
            self.spinBox_first_entry.setEnabled(False)
        else:
            self.radioButton_playlist.setEnabled(False)
            self.radioButton_video.setEnabled(False)
            self.uncheck_buttons()
            self.label_first_entry.setEnabled(False)
            self.spinBox_first_entry.setEnabled(False)

    def uncheck_buttons(self):
        #wierd hack to uncheck radio buttons
        self.radioButton_playlist.setAutoExclusive(False)
        self.radioButton_video.setAutoExclusive(False)
        self.radioButton_playlist.setChecked(False)
        self.radioButton_video.setChecked(False)
        self.radioButton_playlist.setAutoExclusive(True)
        self.radioButton_video.setAutoExclusive(True)

app=QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setWindowTitle("CipherDrive")
widget.resize(700,250)
widget.show()
sys.exit(app.exec_())