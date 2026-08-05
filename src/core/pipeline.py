from core.detect import Detector
from core.ai_report import generate_ai_report
from config import MODEL_PATH


class Pipeline:

    def __init__(self):
        self.detector = Detector(MODEL_PATH)

    def process_image(self, image_path):
        detection_result = self.detector.detect(image_path)
        detection_result["ai_report"] = generate_ai_report(detection_result)
        return detection_result