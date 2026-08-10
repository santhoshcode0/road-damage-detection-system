from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "runs" / "detect" / "models" / "production" / "best.pt"

CONFIDENCE_THRESHOLD = 0.25

UPLOAD_FOLDER = PROJECT_ROOT / "storage" / "uploads"

OUTPUT_FOLDER = PROJECT_ROOT / "storage" / "outputs"