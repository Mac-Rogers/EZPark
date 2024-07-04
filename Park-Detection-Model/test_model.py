import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('model-training_0/weights/best.pt')

# Load the image
image_path = "processed_images/parking_space235.jpg"  # specify file location
image = cv2.imread(image_path)
threshold = .7

if image is not None:
    # Run YOLOv8 inference on the image
    results = model.predict(source=image_path)

    print("Results:", results[0].obb)
    for detection in results[0].obb.conf.tolist():
        if detection > threshold:
            print("Park detected!")
    annotated_image = results[0].plot()

    # Display the annotated image
    cv2.imshow("YOLOv8 Inference", annotated_image)

    # Wait for a key press and close the display window
    cv2.waitKey(0)
    cv2.destroyAllWindows()