from pathlib import Path
import shutil

import cv2
from ultralytics import YOLO

from config import CONFIDENCE_THRESHOLD, OUTPUT_FOLDER


# --------------------------------------------------
# Detection settings
# --------------------------------------------------

DUPLICATE_IOU_THRESHOLD = 0.50


class Detector:

    def __init__(self, model_path):
        self.model = YOLO(model_path)

    # --------------------------------------------------
    # Calculate IoU between two bounding boxes
    # --------------------------------------------------

    @staticmethod
    def calculate_iou(box_a, box_b):

        ax1, ay1, ax2, ay2 = box_a
        bx1, by1, bx2, by2 = box_b

        intersection_x1 = max(ax1, bx1)
        intersection_y1 = max(ay1, by1)
        intersection_x2 = min(ax2, bx2)
        intersection_y2 = min(ay2, by2)

        intersection_width = max(
            0,
            intersection_x2 - intersection_x1
        )

        intersection_height = max(
            0,
            intersection_y2 - intersection_y1
        )

        intersection_area = (
            intersection_width
            * intersection_height
        )

        area_a = (
            max(0, ax2 - ax1)
            * max(0, ay2 - ay1)
        )

        area_b = (
            max(0, bx2 - bx1)
            * max(0, by2 - by1)
        )

        union_area = (
            area_a
            + area_b
            - intersection_area
        )

        if union_area <= 0:
            return 0.0

        return intersection_area / union_area

    # --------------------------------------------------
    # Run detection
    # --------------------------------------------------

    def detect(self, image_path):

        image_path = Path(image_path)

        # --------------------------------------------------
        # Run YOLO detection
        # --------------------------------------------------

        results = self.model.predict(
            source=str(image_path),
            conf=CONFIDENCE_THRESHOLD,
            save=False,
            verbose=False
        )

        # --------------------------------------------------
        # Safely obtain first result
        # --------------------------------------------------

        result = (
            results[0]
            if results
            else None
        )

        # --------------------------------------------------
        # Extract raw detections
        # --------------------------------------------------

        raw_detections = []

        if result is not None and result.boxes is not None:

            for box in result.boxes:

                damage_type = result.names[
                    int(box.cls)
                ]

                confidence = round(
                    float(box.conf),
                    4
                )

                x1 = round(
                    float(box.xyxy[0][0]),
                    2
                )

                y1 = round(
                    float(box.xyxy[0][1]),
                    2
                )

                x2 = round(
                    float(box.xyxy[0][2]),
                    2
                )

                y2 = round(
                    float(box.xyxy[0][3]),
                    2
                )

                raw_detections.append({

                    "damage_type": damage_type,

                    "confidence": confidence,

                    "bounding_box": {

                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2

                    }
                })

        # --------------------------------------------------
        # Remove duplicate detections
        #
        # Detections are compared only when they belong
        # to the same damage class.
        # --------------------------------------------------

        detections = []

        sorted_detections = sorted(
            raw_detections,
            key=lambda x: x["confidence"],
            reverse=True
        )

        for detection in sorted_detections:

            current_type = (
                detection["damage_type"]
            )

            current_box = (
                detection["bounding_box"]
            )

            current_coordinates = (
                current_box["x1"],
                current_box["y1"],
                current_box["x2"],
                current_box["y2"]
            )

            is_duplicate = False

            for existing in detections:

                if (
                    existing["damage_type"]
                    != current_type
                ):
                    continue

                existing_box = (
                    existing["bounding_box"]
                )

                existing_coordinates = (
                    existing_box["x1"],
                    existing_box["y1"],
                    existing_box["x2"],
                    existing_box["y2"]
                )

                iou = self.calculate_iou(
                    current_coordinates,
                    existing_coordinates
                )

                if iou >= DUPLICATE_IOU_THRESHOLD:

                    is_duplicate = True
                    break

            if not is_duplicate:

                detections.append(
                    detection
                )

        # --------------------------------------------------
        # Save annotated image
        # --------------------------------------------------

        annotated_folder = (
            OUTPUT_FOLDER / "annotated"
        )

        annotated_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        annotated_image = (
            annotated_folder
            / image_path.name
        )

        # --------------------------------------------------
        # Damage detected
        # --------------------------------------------------

        if result is not None and len(result.boxes) > 0:

            annotated_frame = result.plot(
                conf=False
            )

            save_success = cv2.imwrite(
                str(annotated_image),
                annotated_frame
            )

            if not save_success:

                raise RuntimeError(
                    "The annotated road image "
                    "could not be saved."
                )

        # --------------------------------------------------
        # No damage detected
        # --------------------------------------------------

        else:

            shutil.copy2(
                image_path,
                annotated_image
            )

        # --------------------------------------------------
        # Return detection result
        # --------------------------------------------------

        return {

            "success": True,

            "original_image": str(
                image_path
            ),

            "annotated_image": str(
                annotated_image
            ),

            "total_damages": len(
                detections
            ),

            "detections": detections

        }