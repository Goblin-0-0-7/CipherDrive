import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi
from threading import Thread
import Hellpers as hell
import YTCS

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("YTCS GUI.ui", self)
        self.toolButton_choose_dir.clicked.connect(self.choose_dir)
        self.pushButton_download.clicked.connect(self.start_download)

    def choose_dir(self):
        dir = QFileDialog.getExistingDirectory(self, "Choose Save Directory", hell.get_work_dir())
        self.lineEdit_save_dir.setText(dir)
    
    def start_download(self):
        url = self.lineEdit_url.text()
        dir = self.lineEdit_save_dir.text()
        video_flag = self.checkBox_video.isChecked()
        audio_flag = self.checkBox_audio.isChecked()
        if url and dir:
            download_thread = Thread(target=YTCS.download_url, args=(url, dir, video_flag, audio_flag), daemon=True)
            download_thread.start()

app=QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.resize(800,600)
widget.show()
sys.exit(app.exec_())