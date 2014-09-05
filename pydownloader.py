#!/usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

import urllib.request

class Downloader(QDialog):

    def __init__(self):
        QDialog.__init__(self)

        layout = QVBoxLayout()

        self.url = QLineEdit()
        self.save_location = QLineEdit()
        browse = QPushButton("Browse")
        self.progress = QProgressBar()
        download = QPushButton("Download")

        self.url.setPlaceholderText("URL")
        self.save_location.setPlaceholderText("File save location")

        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.url)
        layout.addWidget(self.save_location)
        layout.addWidget(browse)
        layout.addWidget(self.progress)
        layout.addWidget(download)

        self.setLayout(layout)

        self.setWindowTitle("PyDownloader")
        #set the focus on the entire app so that the cursor is not set to the
        #first QLineEdit box
        self.setFocus()

        download.clicked.connect(self.download)
        browse.clicked.connect(self.browse_file)

    def download(self):
        url = self.url.text()
        save_location = self.save_location.text()
        try:
            urllib.request.urlretrieve(url, save_location, self.report)
        except Exception:
            QMessageBox.warning(self, "Warning", "The download failed")
            return

        QMessageBox.information(self, "Information", "The download is complete")
        self.progress.setValue(0)
        self.url.setText("")
        self.save_location.setText("")

    def browse_file(self):
        save_file = QFileDialog.getSaveFileName(self, caption="Save File As",
                                                directory=".", filter="All Files (*.*)")
        self.save_location.setText(QDir.toNativeSeparators(save_file))

    def report(self, blocknum, blocksize, totalsize):
        read_so_far = blocknum * blocksize
        if totalsize > 0:
            percent = read_so_far * 100 / totalsize
            self.progress.setValue(int(percent))

app = QApplication(sys.argv)
dl = Downloader()
dl.show()
app.exec_()
