from ultralytics import YOLO


def main():
    model = YOLO("models/trained/run_02/best.pt")

    model.train(
        data="data/RDD_SPLIT/data.yaml",
        epochs=40,
        imgsz=640,
        batch=8,
        project="outputs",
        name="road_damage_detection_run03",
        device=0,
        workers=2
    )

    print("Training completed!")


if __name__ == "__main__":
    main()