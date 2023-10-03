import platform
import numpy as np
import cv2
from PIL import Image, ImageFont, ImageDraw
from PyQt5.QtCore import QThread, pyqtSignal

class DetectThread(QThread):
    callback=pyqtSignal(object)
    def __init__(self, model, file, parent=None):
        super().__init__(parent)
        self.model=model
        self.file=file

    def text(self, img, text, xy=(0, 0), color=(0, 0, 0), size=12):
        pil = Image.fromarray(img)
        s = platform.system()
        if s == "Linux":
            font = ImageFont.truetype(
                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
                size)
        elif s == "Darwin":
            font = ImageFont.truetype('....', size)
        else:
            font = ImageFont.truetype('simsun.ttc', size)
        ImageDraw.Draw(pil).text(xy, text, font=font, fill=color)
        return np.asarray(pil)

    def run(self):
        img = cv2.imdecode(
            np.fromfile(self.file, dtype=np.uint8),
            cv2.IMREAD_UNCHANGED)[:,:,::-1].copy()
        results = self.model.predict(img)[0]
        names = [results.names[int(i.cpu().numpy())] for i in results.boxes.cls]
        boxes = results.boxes.xyxy

        for box, name in zip(boxes, names):
            box = box.cpu().numpy()
            x1 = int(box[0]);y1 = int(box[1]);x2 = int(box[2]);y2 = int(box[3])
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            img = self.text(img, name, (x1, y1 - 20), color=(0, 0, 255), size=50)
        self.callback.emit(img)
