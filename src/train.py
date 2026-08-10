from ultralytics import YOLO


def main():
    model = YOLO("models/trained/run_03/last.pt")

    model.train(
        data="data/RDD_SPLIT/data.yaml",
        epochs=40,
        imgsz=960,
        batch=4,
        project="models/trained",
        name="run_04",
        device=0,
        workers=0,
        patience=10
    )

    print("Training completed!")


if __name__ == "__main__":
    main()