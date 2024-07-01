import cv2
import numpy as np
import os

def apply_perspective_transform(input_image, output_path, scale=1.0):
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

    # Save the resulting image
    cv2.imwrite(output_path, result)
    print(f"Transformed image saved to {output_path}")

def apply_binary_threshold(image, threshold=230):
    # Apply binary thresholding
    _, black_and_white_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return black_and_white_image

def process_images(input_folder, output_folder, scale, threshold=230):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Construct full file path
            file_path = os.path.join(input_folder, filename)
            # Read the image
            image = cv2.imread(file_path)

            if image is None:
                print(f"Could not open or find the image {file_path}.")
                continue

            # Convert to grayscale before applying threshold
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply binary thresholding
            black_and_white_image = apply_binary_threshold(gray_image, threshold=threshold)

            # Construct the output file path
            output_file_path = os.path.join(output_folder, filename)

            # Apply perspective transform
            apply_perspective_transform(black_and_white_image, output_file_path, scale=scale)

            print(f"Processed and saved {output_file_path}")

# Specify the input and output folders
input_folder = 'images'
output_folder = 'processed_images'

# Apply transformations to all images in the input folder and save them in the output folder
process_images(input_folder, output_folder, 2.7, threshold=200)
