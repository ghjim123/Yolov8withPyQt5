import sys
import time
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QListWidgetItem, QFileDialog
from DetectThread import DetectThread
from LoadModelThread import LoadModelThread
from PictureThread import PictureThread
from ui.ui_mainwindow import Ui_MainWindow

class Yolov8App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btnPath.clicked.connect(self.btnPath_click)
        self.lblPath.setText("C:/")
        self.path=self.lblPath.text()
        self.lblStatus.setText("載入模型中, 請稍後...")
        self.loadModelThread=LoadModelThread()
        self.loadModelThread.callback.connect(self.loadModelThreadCallback)
        self.loadModelThread.start()

    # 載入模型
    def loadModelThreadCallback(self, model):
        self.model=model
        self.lblStatus.setText("")
        self.pictureThread=PictureThread(self.path)
        self.pictureThread.callback.connect(self.pictureThreadCallback)
        self.pictureThread.start()

    # 載入圖片
    def pictureThreadCallback(self, pix):
        btn=QPushButton()
        btn.setIcon(QIcon(pix))
        btn.setIconSize(QSize(400,300))
        btn.tag=pix.tag
        btn.clicked.connect(self.btn_click)
        item=QListWidgetItem()
        item.setSizeHint(QSize(400,300))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, btn)

    # 按鈕(=圖片)點擊觸發事件
    def btn_click(self):
        btn=self.sender()
        self.lblStatus.setText('yolov8 辨識中....')
        self.t1=time.time()
        self.detectThread=DetectThread(self.model, btn.tag)
        self.detectThread.callback.connect(self.detectThreadCallback)
        self.detectThread.start()

    # 辨識圖片
    def detectThreadCallback(self, img):
        self.t2=time.time()
        self.lblStatus.setText(f'偵測時間 : {self.t2-self.t1:.7f}秒')
        pix=QPixmap(
            QImage(img,
                   img.shape[1],
                   img.shape[0],
                   img.shape[1]*3,
                   QImage.Format_RGB888
                   )
        )
        w=pix.width()
        h=pix.height()
        r=w/h
        label_width=self.lblImg.width()
        label_height=self.lblImg.height()
        label_r=label_width/label_height
        if r>label_r:
            pix=pix.scaled(label_width, label_width/r)
        else:
            pix=pix.scaled(label_height *r, label_height)
        self.lblImg.setPixmap(pix)

    # 載入資料夾
    def btnPath_click(self):
        self.path=QFileDialog.getExistingDirectory()
        if self.path!='':
            self.path=self.path.replace("\\","/")
            self.lblPath.setText(self.path)
            self.listWidget.clear()
            self.pictureThread=PictureThread(self.path)
            self.pictureThread.callback.connect(self.pictureThreadCallback)
            self.pictureThread.start()


if __name__=='__main__':
    app=QApplication(sys.argv)
    mainWindow=Yolov8App()
    mainWindow.showMaximized()
    app.exec()