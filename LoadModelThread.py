from PyQt5.QtCore import QThread, pyqtSignal
from ultralytics import YOLO

class LoadModelThread(QThread):
    #底下的 callback 是類別變數, 但經過 __init__後，會轉換成物件變數
    #這一段網路上查不到，只有官網才有說明
    callback=pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
    def run(self):
        model=YOLO("./yolov8n.pt")
        self.callback.emit(model)