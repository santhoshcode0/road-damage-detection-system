from core.detect import Detector
from core.damage_assessment import assess_damage
from core.ai_report import generate_ai_report

from config import MODEL_PATH


class Pipeline:

    def __init__(self):

        # --------------------------------------------------
        # Initialize detector
        # --------------------------------------------------

        self.detector = Detector(
            MODEL_PATH
        )

    def process_image(self, image_path):

        # --------------------------------------------------
        # Step 1: Detect visible road damage
        # --------------------------------------------------

        detection_result = (
            self.detector.detect(
                image_path
            )
        )

        # --------------------------------------------------
        # Step 2: Perform structured assessment
        # --------------------------------------------------

        assessment = assess_damage(
            detection_result
        )

        # --------------------------------------------------
        # Step 3: Attach assessment
        # --------------------------------------------------

        detection_result[
            "assessment"
        ] = assessment

        # --------------------------------------------------
        # Step 4: Generate professional report
        # --------------------------------------------------

        ai_report = generate_ai_report(
            detection_result,
            assessment
        )

        # --------------------------------------------------
        # Step 5: Attach AI report
        # --------------------------------------------------

        detection_result[
            "ai_report"
        ] = ai_report

        # --------------------------------------------------
        # Return complete result
        # --------------------------------------------------

        return detection_result