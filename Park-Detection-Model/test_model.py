import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('runs/detect/train5/weights/best.pt')

# Load the image
image_path = "test/image_name.jpg" #specify file location
image = cv2.imread(image_path)

if image is not None:
    # Run YOLOv8 inference on the image
    results = model(image)

    # Visualize the results on the image
    annotated_image = results[0].plot()

    # Display the annotated image
    cv2.imshow("YOLOv8 Inference", annotated_image)

    # Wait for a key press and close the display window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Could not open or find the image.")
