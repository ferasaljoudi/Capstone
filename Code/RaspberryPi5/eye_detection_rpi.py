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

# Function to preprocess the eye before predicting it with the model
# This function will resize the image, convert it to RGB and normalize pixel values
# These steps are required to match the model input we have
def prepare_eye_for_model(eye_img):
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
def get_box(landmarks, ids, width, height, margin=11):
    x_coords = [int(landmarks[id].x * width) for id in ids]
    y_coords = [int(landmarks[id].y * height) for id in ids]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    return x_min - margin, y_min - (margin * 2), x_max + margin, y_max + margin

# Open the video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

print("Press 'q' to quit.")

# Default variables
closed_start_time = None
sleepy_detected = False

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
            # Draw the rectangle around the left eye with green color and 2px thickness
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            # Extract the rectangle region as a new cropped image
            left_eye_crop = frame[y_min:y_max, x_min:x_max]

            # Right eye landmarks
            right_eye_ids = [263, 362, 387, 373, 374, 380, 381, 382, 384, 386, 388]
            # Get the eye region through the get_box function
            x_min, y_min, x_max, y_max = get_box(face_landmarks.landmark, right_eye_ids, frame_width, frame_height)
            # Draw the rectangle around the right eye with green color and 2px thickness
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
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

    if eye_status == "Closed":
        if closed_start_time is None:
            # Initialize the timer to track for how long the status will stay "Closed"
            closed_start_time = time.time()
        # If status stayed "Closed" for 2 seconds, sleepy is detected
        elif time.time() - closed_start_time >= 2 and not sleepy_detected:
            sleepy_detected = True

    # If status is not, reset "closed_start_time" & "sleepy_detected"
    else:
        closed_start_time = None
        sleepy_detected = False

    # Display the status on the top left corner
    color = (0, 0, 255) if eye_status == "Closed" else (0, 255, 0)
    # Add the text to the frame (start at 30 from left and 50 from top)
    # With 1 as font scale and 2 as thickness
    cv2.putText(frame, eye_status, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    if sleepy_detected:
        # Display "Sleepy detected" (start at 30 from left and 100 from top)
        # With 1 as font scale and 2 as thickness
        cv2.putText(frame, "Sleepy detected", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        

    # Show the video feed
    cv2.imshow("Live Eye Detection", frame)

    # Break if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
