import cv2
import numpy as np
from ultralytics import YOLO

def apply_perspective_transform(input_image, scale=1.0):
    height, width = input_image.shape[:2]

    # Define the four points in the source image
    pts_src = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

    # Define the four points in the destination image
    pts_dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1 - scale * 100, height - 1],
        [scale * 100, height - 1]
    ], dtype=np.float32)

    # Calculate the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

    # Apply the perspective transformation
    result = cv2.warpPerspective(input_image, matrix, (width, height))

    return result

def apply_binary_threshold(image, threshold=230):
    # Apply binary thresholding
    _, black_and_white_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return black_and_white_image

def process_webcam_feed(scale=1.0, threshold=230):
    # Load the YOLOv8 model
    model = YOLO('model-training_0/weights/best.pt')

    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # Convert to grayscale before applying threshold
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        black_and_white_image = apply_binary_threshold(gray_image, threshold=threshold)

        # Apply perspective transform
        transformed_image = apply_perspective_transform(black_and_white_image, scale=scale)

        # Convert the transformed image back to BGR
        transformed_image_bgr = cv2.cvtColor(transformed_image, cv2.COLOR_GRAY2BGR)

        # Run YOLOv8 inference on the transformed image
        results = model(transformed_image_bgr)
        print("Results ",results[0].obb.conf.tolist())

        # Visualize the results on the transformed image
        annotated_frame = results[0].plot()

        # Display the original and processed frames
        cv2.imshow('Original', frame)
        cv2.imshow('Processed', annotated_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Adjust the scale factor and threshold to control the perspective correction and binary thresholding
    scale_factor = 2.7
    threshold_value = 200

    process_webcam_feed(scale=2.7, threshold=200)
