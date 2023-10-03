from PyQt5.QtCore import QThread, pyqtSignal
from ultralytics import YOLO

class LoadModelThread(QThread):
    callback=pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        model=YOLO("./yolov8n.pt")
        self.callback.emit(model)