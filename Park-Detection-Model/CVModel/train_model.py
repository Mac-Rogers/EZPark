from ultralytics import YOLO

model = YOLO("yolov8n-obb.pt")

results = model.train(data="config.yaml", epochs=40, imgsz=640)