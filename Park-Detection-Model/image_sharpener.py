import cv2

def convert_to_black_and_white(image_path, threshold):
    # Load the image in grayscale mode
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Could not open or find the image.")
        return

    # Apply binary thresholding
    _, black_and_white_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    # Display the original and black-and-white images
    cv2.imshow('Original Grayscale Image', image)
    cv2.imshow('Black and White Image', black_and_white_image)

    # Save the black and white image
    output_path = 'black_and_white_image.jpg'
    cv2.imwrite(output_path, black_and_white_image)
    print(f"Black and white image saved as {output_path}")

    # Wait until a key is pressed and close all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Path to your image
image_path = 'images/parking_space60.jpg'

# Adjust the threshold value as needed (0-255)
threshold_value = 230

convert_to_black_and_white(image_path, threshold_value)
