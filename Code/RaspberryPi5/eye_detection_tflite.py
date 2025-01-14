import os
import time

import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
# Detect and track the face with at least 80% of accuracy
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Load the model
path_for_model = "model.tflite"
# Initialize the TensorFlow Lite Interpreter
interpreter = tf.lite.Interpreter(path_for_model)
# Allocate memory for the model's input and output tensors
interpreter.allocate_tensors()

# Get metadata about the model's input and output tensors, including shape, data type, and index
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Landmarks for the lips
upper_lip_top = 13
lower_lip_bottom = 14
lip_left = 61
lip_right = 291

# Function to preprocess the eye before predicting it with the model
# This function will resize the image, convert it to RGB and normalize pixel values
# These steps are required to match the model input we have
def prepare_eye_for_model(eye_img):
    # Validate input is a NumPy array
    if not isinstance(eye_img, np.ndarray):
        raise ValueError("Input must be a NumPy array representing an image.")
    # Validate the image contains pixel data
    if eye_img.size == 0:
        raise ValueError("Input image can not be empty.")
    eye_img = cv2.resize(eye_img, (48, 48))
    eye_img = cv2.cvtColor(eye_img, cv2.COLOR_BGR2RGB)
    eye_img = eye_img / 255.0
    eye_img = np.expand_dims(eye_img, axis=0).astype(np.float32)
    return eye_img

# Function to calculate a bounding box with margin.
# This function is to isolates the eye region,
# so not the entire frame is used to be processed with the model.
# The result frame of this box is the area of the eye being processed with the model.
# The margin value was determined through a few experiments.
def get_box(landmarks, ids, width, height, margin=10):
    # Ids should be a list of integers
    if not all(isinstance(id, int) for id in ids):
        raise ValueError("IDs must be a list of integers.")
    
    # Width and height should be positive numbers
    if not isinstance(width, (int, float)) or width <= 0:
        raise ValueError("Width must be a positive number.")
    if not isinstance(height, (int, float)) or height <= 0:
        raise ValueError("Height must be a positive number.")
    x_coords = [int(landmarks[id].x * width) for id in ids]
    y_coords = [int(landmarks[id].y * height) for id in ids]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    return x_min - margin, y_min - (margin * 2), x_max + margin, y_max + margin

def calculate_mouth_ratio(upper_lip, lower_lip, left_lip, right_lip):
    # Calculate vertical and horizontal distances
    vertical = np.linalg.norm(np.array(upper_lip) - np.array(lower_lip))
    horizontal = np.linalg.norm(np.array(left_lip) - np.array(right_lip))
    if horizontal == 0:
        raise ValueError("Horizontal distance can not be zero.")
    # Return mouth aspect ratio
    return (vertical / horizontal) * 100

# Function to check if yawn is detected
def detect_yawn(average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert, threshold=30, duration=2):
    # Check the lip average stayed at (or more than) threshold for 2 seconds
    if average_ratio_lips >= threshold:
        if yawn_start_time is None:
            # Initialize the timer to track for how long the mouth is open
            yawn_start_time = time.time()
        elif time.time() - yawn_start_time >= duration and not yawn_detected:
            # If mouth stayed open for 2 seconds, yawn is detected
            yawn_detected = True
            yawn_alert = True
    else:
        # Reset variables if the ratio falls below the threshold
        yawn_start_time = None
        yawn_detected = False
        yawn_alert = False

    # Return the updated (yawn_start_time, yawn_detected, yawn_alert)
    return yawn_start_time, yawn_detected, yawn_alert

# Function to check if sleepy is detected
def detect_eye_closure(eye_status, closed_start_time, sleepy_detected, closed_alert, duration=1):
    if eye_status == "Closed":
        if closed_start_time is None:
            # Initialize the timer to track for how long the status will stay "Closed"
            closed_start_time = time.time()
        # If status stayed "Closed" for 1 seconds, sleepy is detected
        elif time.time() - closed_start_time >= duration and not sleepy_detected:
            sleepy_detected = True
            closed_alert = True
    # If status is not, reset variables
    else:
        closed_start_time = None
        sleepy_detected = False
        closed_alert = False

    # Return the updated (closed_start_time, sleepy_detected, closed_alert)
    return closed_start_time, sleepy_detected, closed_alert

# Function to play yawn alert
def yawn_alert_func(yawn_start_time, yawn_detected, yawn_alert, file2):
    if yawn_detected and yawn_alert:
        # Play the yawn_alert
        os.system(f"mpg321 {file2}")
        # Reset variables
        yawn_start_time = None
        yawn_detected = False
        yawn_alert = False
    return yawn_start_time, yawn_detected, yawn_alert

# Function to play closed alert
def closed_alert_func(closed_start_time, sleepy_detected, closed_alert, file1):
    if sleepy_detected and closed_alert:
        # Play the closed_alert
        os.system(f"mpg321 {file1}")
        # Reset variables
        closed_start_time = None
        sleepy_detected = False
        closed_alert = False
    return closed_start_time, sleepy_detected, closed_alert

# Main logic
def main():
    # Lists to store mouth ratio
    list_of_lips_ratios = []

    # Open the video
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        exit()

    print("Press 'q' to quit.")

    # Audio file paths
    file1 = "focus_on_the_road.mp3"
    file2 = "consider_taking_a_rest.mp3"
    file3 = "detection_system_on.mp3"
    file4 = "detection_system_off.mp3"

    # Default variables
    closed_start_time = None
    yawn_start_time = None
    sleepy_detected = False
    yawn_detected = False
    closed_alert = False
    yawn_alert = False

    # Play system is on
    os.system(f"mpg321 {file3}")

    while True:
        success, frame = cap.read()
        if not success:
            print("Error: Can not read frame.")
            break

        # Convert frame to RGB since MediaPipe requires RGB input
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Extract the height and width of the frame and ignore the color channels
        frame_height, frame_width, _ = frame.shape

        # Process the frame with MediaPipe Face Mesh
        results = face_mesh.process(rgb_frame)

        # Default status
        eye_status = "Open"

        # Check if any faces are detected in the frame
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Left eye landmarks
                left_eye_ids = [33, 133, 160, 144, 145, 153, 154, 155, 157, 159, 161]
                # Get the eye region through the get_box function
                x_min, y_min, x_max, y_max = get_box(face_landmarks.landmark, left_eye_ids, frame_width, frame_height)
                # Extract the rectangle region as a new cropped image
                left_eye_crop = frame[y_min:y_max, x_min:x_max]

                # Right eye landmarks
                right_eye_ids = [263, 362, 387, 373, 374, 380, 381, 382, 384, 386, 388]
                # Get the eye region through the get_box function
                x_min, y_min, x_max, y_max = get_box(face_landmarks.landmark, right_eye_ids, frame_width, frame_height)
                # Extract the rectangle region as a new cropped image
                right_eye_crop = frame[y_min:y_max, x_min:x_max]

                # Predict eye states
                if left_eye_crop.size > 0 and right_eye_crop.size > 0:
                    # Process both eyes images
                    left_eye_processed = prepare_eye_for_model(left_eye_crop)
                    right_eye_processed = prepare_eye_for_model(right_eye_crop)

                    # Set the preprocessed left eye image as input to the model
                    interpreter.set_tensor(input_details[0]['index'], left_eye_processed)
                    # Process the input data through the model
                    interpreter.invoke()
                    # Get the model's output for the left eye
                    # np.argmax extracts the predicted class with the highest probability
                    left_eye_pred = np.argmax(interpreter.get_tensor(output_details[0]['index']))

                    # Set the preprocessed right eye image as input to the model
                    interpreter.set_tensor(input_details[0]['index'], right_eye_processed)
                    # Process the input data through the model
                    interpreter.invoke()
                    # Get the model's output for the right eye
                    # np.argmax extracts the predicted class with the highest probability
                    right_eye_pred = np.argmax(interpreter.get_tensor(output_details[0]['index']))

                    # The status will be "Closed" if both eyes are closed
                    if left_eye_pred == 0 and right_eye_pred == 0:
                        eye_status = "Closed"
                
                # Call the detect_eye_closure function to check if closed eyes are detected
                closed_start_time, sleepy_detected, closed_alert = detect_eye_closure(eye_status, closed_start_time, sleepy_detected, closed_alert)

                # Call the closed alert function
                closed_start_time, sleepy_detected, closed_alert = closed_alert_func(closed_start_time, sleepy_detected, closed_alert, file1)
                
                # Get frame dimensions for scaling landmarks
                h, w, _ = frame.shape
                
                # Process lips
                upper_lip = face_landmarks.landmark[upper_lip_top]
                lower_lip = face_landmarks.landmark[lower_lip_bottom]
                left_lip = face_landmarks.landmark[lip_left]
                right_lip = face_landmarks.landmark[lip_right]

                # Convert lip landmarks to pixel coordinates
                upper_lip_point = (int(upper_lip.x * w), int(upper_lip.y * h))
                lower_lip_point = (int(lower_lip.x * w), int(lower_lip.y * h))
                left_lip_point = (int(left_lip.x * w), int(left_lip.y * h))
                right_lip_point = (int(right_lip.x * w), int(right_lip.y * h))

                # Get the mouth aspect ratio
                lip_ratio = calculate_mouth_ratio(upper_lip_point, lower_lip_point, left_lip_point, right_lip_point)
                list_of_lips_ratios.append(lip_ratio)
                # Only the most recent 3 values are kept
                if len(list_of_lips_ratios) > 3:
                    list_of_lips_ratios.pop(0)
                # Average mouth aspect ratio
                average_ratio_lips = sum(list_of_lips_ratios) / len(list_of_lips_ratios)

                # Call the detect_yawn function to check if yawn detected
                yawn_start_time, yawn_detected, yawn_alert = detect_yawn(average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert)
                
                # Call the yawn alert function
                yawn_start_time, yawn_detected, yawn_alert = yawn_alert_func(yawn_start_time, yawn_detected, yawn_alert, file2)

        # Break if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Play system is off
            os.system(f"mpg321 {file4}")
            break

    # Release the video capture
    cap.release()
    face_mesh.close()

if __name__ == "__main__":
    main()
