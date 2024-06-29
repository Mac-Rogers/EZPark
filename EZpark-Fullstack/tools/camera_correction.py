import cv2
import numpy as np

# Load the image
image = cv2.imread('images/parking_space95.jpg')
height, width = image.shape[:2]

# Define the four points in the source image
# These points are in the order: top-left, top-right, bottom-right, bottom-left
pts_src = np.array([[173, 291], [322, 293], [400, 370], [136, 367]], dtype=np.float32)

# Define the four points in the destination image
# These points should form a perfect rectangle
pts_dst = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)

# Calculate the perspective transform matrix
matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

# Apply the perspective transformation
result = cv2.warpPerspective(image, matrix, (width, height))

# Save and display the result
cv2.imwrite('output.jpg', result)
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
