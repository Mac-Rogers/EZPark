import cv2
import os

def apply_binary_threshold(input_folder, output_folder, threshold=230):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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

            # Construct the output file path
            output_file_path = os.path.join(output_folder, filename)
            # Save the processed image in the output folder
            cv2.imwrite(output_file_path, black_and_white_image)
            print(f"Processed and saved {output_file_path}")

# Specify the input and output folders
input_folder = 'images'
output_folder = 'processed_images'

# Apply binary threshold to all images in the input folder and save them in the output folder
apply_binary_threshold(input_folder, output_folder, threshold=230)
