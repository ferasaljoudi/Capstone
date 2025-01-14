import os
import time

import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Landmarks for left and right eyes
left_eye_ids = [159, 23, 130, 243]
right_eye_ids = [386, 374, 263, 362]

# Landmarks for the lips
upper_lip_top = 13
lower_lip_bottom = 14
lip_left = 61
lip_right = 291

# Function to calculate the eye aspect ratio for a given eye
def calculate_eye_ratio(coords):
    if len(coords) != 4:
        # Default high value if landmarks are missing
        return 100
    # Calculate vertical and horizontal distances
    vertical_distance = np.linalg.norm(np.array(coords[0]) - np.array(coords[1]))
    horizontal_distance = np.linalg.norm(np.array(coords[2]) - np.array(coords[3]))
    # Return eye aspect ratio
    return (vertical_distance / horizontal_distance) * 100

# Function to calculate the mouth aspect ratio
def calculate_mouth_ratio(upper_lip, lower_lip, left_lip, right_lip):
    # Calculate vertical and horizontal distances
    vertical = np.linalg.norm(np.array(upper_lip) - np.array(lower_lip))
    horizontal = np.linalg.norm(np.array(left_lip) - np.array(right_lip))
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

# Function to check if closed eyes are detected
def detect_eye_closure(average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=24, duration=1):
    # Check the eye closed based on if the average stayed at (or less than) threshold for 1 seconds
    if average_ratio_eyes <= threshold:
        if closed_start_time is None:
            # Initialize the timer to track for how long the eyes are closed
            closed_start_time = time.time()
        elif time.time() - closed_start_time >= duration and not sleepy_detected:
            sleepy_detected = True
            closed_alert = True
    else:
        # If average went above the threshold, reset variables
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
    # Lists to store eye and mouth ratios
    list_of_left_eye_ratios = []
    list_of_right_eye_ratios = []
    list_of_lips_ratios = []

    blink_counter = 0
    counter = 0

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
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        # Check if any faces are detected in the frame
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Get frame dimensions for scaling landmarks
                h, w, _ = frame.shape

                # Process left eye
                left_coords = []
                for id in left_eye_ids:
                    # Convert the normalized landmark coordinates (range 0 to 1) to pixel positions
                    x = int(face_landmarks.landmark[id].x * w)
                    y = int(face_landmarks.landmark[id].y * h)
                    left_coords.append((x, y))

                # Get the left eye ratio
                left_eye_ratio = calculate_eye_ratio(left_coords)
                list_of_left_eye_ratios.append(left_eye_ratio)
                # Only the most recent 3 values are kept
                if len(list_of_left_eye_ratios) > 3:
                    list_of_left_eye_ratios.pop(0)
                # Average aspect ratio for the most recent 3 values
                ratio_average_left = sum(list_of_left_eye_ratios) / len(list_of_left_eye_ratios)

                # Process right eye
                right_coords = []
                for id in right_eye_ids:
                    # Convert the normalized landmark coordinates (range 0 to 1) to pixel positions
                    x = int(face_landmarks.landmark[id].x * w)
                    y = int(face_landmarks.landmark[id].y * h)
                    right_coords.append((x, y))

                # Get the right eye ratio
                right_eye_ratio = calculate_eye_ratio(right_coords)
                list_of_right_eye_ratios.append(right_eye_ratio)
                # Only the most recent 3 values are kept
                if len(list_of_right_eye_ratios) > 3:
                    list_of_right_eye_ratios.pop(0)
                # Average aspect ratio for the most recent 3 values
                ratio_average_right = sum(list_of_right_eye_ratios) / len(list_of_right_eye_ratios)

                # Calculate average eye ratio for both eyes
                average_ratio_eyes = (ratio_average_left + ratio_average_right) / 2

                # Check blink condition and increment the blink counter if average 25 or less
                if average_ratio_eyes <= 25 and counter == 0:
                    blink_counter += 1
                    counter = 1
                if counter != 0:
                    counter += 1
                    # Reset counter after a delay
                    if counter > 10:
                        counter = 0

                # Call the detect_eye_closure function to check if closed eyes are detected
                closed_start_time, sleepy_detected, closed_alert = detect_eye_closure(average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert)

                # Call the closed alert function
                closed_start_time, sleepy_detected, closed_alert = closed_alert_func(closed_start_time, sleepy_detected, closed_alert, file1)

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
