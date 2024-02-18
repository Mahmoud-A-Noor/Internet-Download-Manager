from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

import os
from os import path
import sys
import urllib.request
import pafy
import humanize


FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI.ui"))

class mainapp(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(mainapp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI()
        self.Button_Handler()
        self.Theme_Handler()
        self.lineEdit.setPlaceholderText("https://download.sublimetext.com/sublime_text_build_4113_x64_setup.exe")

    def Handle_UI(self):
        self.setWindowTitle("Downloader")
        self.setFixedSize(861,445)

    def Handle_Progress(self,blocknum,blocksize,totalsize):
        read = blocknum * blocksize
        if (totalsize>0):
            percent = (read/totalsize)*100
            self.progressBar.setValue(int(percent))
            QApplication.processEvents()


    def Apply_AMOLED_Style(self):
        style = open('./themes/AMOLED.qss' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_Aqua_Style(self):
        style = open('./themes/Aqua.qss' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_ConsoleStyle_Style(self):
        style = open('./themes/ConsoleStyle.qss' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_ElegantDark_Style(self):
        style = open('./themes/ElegantDark.qss', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_MacOS_Style(self):
        style = open('./themes/MacOS.qss', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_ManjaroMix_Style(self):
        style = open('./themes/ManjaroMix.qss', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_MaterialDark_Style(self):
        style = open('./themes/MaterialDark.qss', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_NeonButtons_Style(self):
        style = open('./themes/NeonButtons.qss', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_Ubuntu_Style(self):
        style = open('./themes/Ubuntu.qss', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Theme_Handler(self):
        self.actionAMOLED.triggered.connect(lambda :self.Apply_AMOLED_Style())
        self.actionAqua.triggered.connect(lambda :self.Apply_Aqua_Style())
        self.actionConsoleStyle.triggered.connect(lambda :self.Apply_ConsoleStyle_Style())
        self.actionElegantDark.triggered.connect(lambda :self.Apply_ElegantDark_Style())
        self.actionMacOS.triggered.connect(lambda :self.Apply_MacOS_Style())
        self.actionManjaroMix.triggered.connect(lambda :self.Apply_ManjaroMix_Style())
        self.actionMaterialDark.triggered.connect(lambda :self.Apply_MaterialDark_Style())
        self.actionNeonButtons.triggered.connect(lambda :self.Apply_NeonButtons_Style())
        self.actionUbuntu.triggered.connect(lambda :self.Apply_Ubuntu_Style())

    def Button_Handler(self):
        self.pushButton_2.clicked.connect(self.Download)
        self.pushButton.clicked.connect(self.Browse)
        self.pushButton_7.clicked.connect(self.Get_Youtube_Video)
        self.pushButton_6.clicked.connect(self.Download_Youtube_Video)
        self.pushButton_5.clicked.connect(self.Download_Youtube_Playlist)
        self.pushButton_3.clicked.connect(self.Video_Directory_Browse)
        self.pushButton_5.clicked.connect(self.Download_Youtube_Playlist)
        self.pushButton_4.clicked.connect(self.Playlist_Directory_Browse)

    def Browse(self):
        save_place = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files (*.*)")
        self.lineEdit_2.setText(str(save_place).split(',')[0][2:-1])

    def Download(self):
        ### https://download.sublimetext.com/sublime_text_build_4113_x64_setup.exe

        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(url, save_location, self.Handle_Progress)
        except Exception:
            QMessageBox.warning(self, "DownloadError", "The Download Failed")
            return
        QMessageBox.information(self, "Download Completed", "The Download Finished")
        self.progressBar.setValue(0)
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")

    def Get_Youtube_Video(self):
        videoLink = self.lineEdit_3.text()
        video = pafy.new(videoLink)
        streams = video.streams
        self.comboBox.clear()
        for stream in streams:
            item = f"{stream.mediatype} [ {stream.extension} ]   {stream.quality}\t {humanize.naturalsize(stream.get_filesize())}"
            self.comboBox.addItem(item)

    def Download_Youtube_Video(self):
        videoLink = self.lineEdit_3.text()
        savedir = self.lineEdit_4.text()
        quality = self.comboBox.currentIndex()

        if videoLink == '' or savedir == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL or save location")
        else:
            video = pafy.new(videoLink)
            streams = video.streams
            streams[quality].download(savedir,callback=self.Video_Progress)
            QMessageBox.information(self, "Download Completed", "The Download Finished")


    def Video_Progress(self , total , received , ratio , rate , time):
        read_data = received
        if total > 0 :
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(int(download_percentage))
            QApplication.processEvents()


    def Video_Directory_Browse(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_4.setText(dir)





    def Download_Youtube_Playlist(self):
        playlistLink = self.lineEdit_6.text()
        savedir = self.lineEdit_5.text()

        if playlistLink == '' or savedir == '' :
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")

        else:
            playlist = pafy.get_playlist(playlistLink)
            videos = playlist['items']

            if(os.path.exists(str(playlist['title']))):
                os.chdir(str(playlist['title']))
            else:
                os.chdir(savedir)
                os.mkdir(str(playlist['title']))
                os.chdir(str(playlist['title']))

            current_video = 1

            for video in videos:
                self.lcdNumber.display(current_video)
                video['pafy'].getbest(preftype='mp4').download(callback=self.Playlist_Progress)
                QApplication.processEvents()
                current_video+=1


    def Playlist_Progress(self , total , received , ratio , rate , time):
        read_data = received
        if total > 0 :
            download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            QApplication.processEvents()


    def Playlist_Directory_Browse(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_5.setText(dir)


def main():
    app = QApplication(sys.argv)
    window = mainapp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()