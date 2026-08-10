import time
from pathlib import Path

from ultralytics import YOLO

from config import CONFIDENCE_THRESHOLD, OUTPUT_FOLDER


class Detector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, image_path):
        start_time = time.time()

        image_path = Path(image_path)

        results = self.model.predict(
            source=str(image_path),
        conf=CONFIDENCE_THRESHOLD,
        save=True,
        project=str(OUTPUT_FOLDER),
        name="annotated",
        exist_ok=True,
        verbose=False,
        show_conf=False
        )

        detections = []

        result = results[0]

        for box in result.boxes:
            detections.append({
                "damage_type": result.names[int(box.cls)],
                "confidence": round(float(box.conf), 4),
                "bounding_box": {
                    "x1": round(float(box.xyxy[0][0]), 2),
                    "y1": round(float(box.xyxy[0][1]), 2),
                    "x2": round(float(box.xyxy[0][2]), 2),
                    "y2": round(float(box.xyxy[0][3]), 2)
                }
            })

        processing_time = round(time.time() - start_time, 3)

        annotated_image = (
            OUTPUT_FOLDER /
            "annotated" /
            image_path.name
        )

        return {
            "success": True,
            "original_image": str(image_path),
            "annotated_image": str(annotated_image),
            "total_damages": len(detections),
            "detections": detections,
            "processing_time": processing_time
        }