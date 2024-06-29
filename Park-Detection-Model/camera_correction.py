import cv2
import numpy as np

def apply_perspective_transform(image_path, output_path, scale=1.0):
    # Load the image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    # Define the four points in the source image
    # These points are in the order: top-left, top-right, bottom-right, bottom-left
    pts_src = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

    # Define the four points in the destination image
    # Adjust these points to create the perspective effect
    pts_dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1 - scale * 100, height - 1],
        [scale * 100, height - 1]
    ], dtype=np.float32)

    # Calculate the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

    # Apply the perspective transformation
    result = cv2.warpPerspective(image, matrix, (width, height))

    # Save the resulting image
    cv2.imwrite(output_path, result)
    print(f"Transformed image saved to {output_path}")

    # Display the original and transformed images
    cv2.imshow('Original Image', image)
    cv2.imshow('Transformed Image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Adjust the scale factor to control the amount of perspective correction
    scale_factor = 2.3
    input_image_path = 'images/parking_space106.jpg'
    output_image_path = 'images/transformed_parking_space.jpg'

    apply_perspective_transform(input_image_path, output_image_path, scale=scale_factor)
