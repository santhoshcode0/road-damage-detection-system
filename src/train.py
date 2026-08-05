from ultralytics import YOLO


def main():
    model = YOLO("models/trained/run_02/last.pt")

    model.train(
        data="data/RDD_SPLIT/data.yaml",
        epochs=20,
        imgsz=640,
        batch=4,
        project="models/trained",
        name="run_03",
        device=0,
        workers=0,
        patience=5
    )

    print("Training completed!")


if __name__ == "__main__":
    main()