import cv2
import os

def apply_binary_threshold(input_folder, threshold=230):
    # List all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Construct full file path
            file_path = os.path.join(input_folder, filename)
            # Read the image in grayscale mode
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            if image is None:
                print(f"Could not open or find the image {file_path}.")
                continue

            # Apply binary thresholding
            _, black_and_white_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

            # Save the processed image, replacing the original
            cv2.imwrite(file_path, black_and_white_image)
            print(f"Processed and replaced {file_path}")

# Specify the input folder
input_folder = 'images'

# Apply binary threshold to all images in the input folder
apply_binary_threshold(input_folder, threshold=230)
