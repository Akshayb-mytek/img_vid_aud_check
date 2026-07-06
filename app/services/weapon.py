from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def check_weapon(frames):
    for frame in frames:
        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]
                print(f"Detected: {label} with confidence {box.conf[0]:.2f}")

                if label in ["knife", "gun"]:
                    return True

    return False
