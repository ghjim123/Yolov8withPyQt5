import os
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

class PictureThread(QThread):
    callback=pyqtSignal(object)
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path=path
        self.runFlag=True

    def run(self):
        ls=os.listdir(self.path)
        files=[]
        for l in ls:
            ll=l.lower()
            if ll.endswith('.jpg') or ll.endswith('.png'):
                files.append(os.path.join(self.path, l))
        index=0
        while index<len(files) and self.runFlag:
            pix=QPixmap(files[index])
            pix=pix.scaled(400,300)
            pix.tag=files[index]
            self.callback.emit(pix)
            index+=1
            QThread.msleep(10)