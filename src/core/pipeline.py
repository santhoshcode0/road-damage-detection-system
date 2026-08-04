from core.detect import Detector
from config import MODEL_PATH


class Pipeline:

    def __init__(self):
        self.detector = Detector(MODEL_PATH)

    def process_image(self, image_path):
        return self.detector.detect(image_path)