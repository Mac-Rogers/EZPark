import cv2
import os
import time

def read_frame_count(file_path):
    try:
        with open(file_path, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def write_frame_count(file_path, count):
    with open(file_path, 'w') as file:
        file.write(str(count))

def capture_frames_from_webcam(output_folder, frame_count_file, interval_ms=300):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read the current frame count
    frame_count = read_frame_count(frame_count_file)

    # Initialize webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            # Save the frame to the specified folder
            filename = os.path.join(output_folder, f"parking_space{frame_count}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Saved {filename}")

            frame_count += 1

            # Update the frame count in the file
            write_frame_count(frame_count_file, frame_count)

            # Wait for the specified interval
            time.sleep(interval_ms / 1000.0)

            # Display the resulting frame (optional)
            cv2.imshow('Webcam Feed', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupted by user.")

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

# Specify the output folder and frame count file
output_folder = 'images'
frame_count_file = 'frame_count.txt'

# Capture frames from the webcam and save them to the specified folder
capture_frames_from_webcam(output_folder, frame_count_file, interval_ms=500)
