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
    if horizontal == 0:
        raise ValueError("Horizontal distance can not be zero.")
    # Return mouth aspect ratio
    return (vertical / horizontal) * 100

# Function to calculate the face turn aspect ratio
def calculate_face_turn_ratio(left_eyebrow, right_eyebrow, left_cheek, right_cheek):
    # Calculate distances
    eyebrows_width = right_eyebrow.x - left_eyebrow.x
    face_width = right_cheek.x - left_cheek.x
    if face_width == 0:
        raise ValueError("Face width distance can not be zero.")
    # Return aspect ratio
    return (eyebrows_width / face_width) * 180

# Function to check if signs are detected
# This function will detect closed eyes, yawning or face turn
def detect_signs(average_ratio, start_time, detected, alert, threshold, duration):
    if threshold == 30:
        # Check if the average stayed at (or MORE than) threshold
        if average_ratio >= threshold:
            if start_time is None:
                # Initialize the timer
                start_time = time.time()
            elif time.time() - start_time >= duration and not detected:
                detected = True
                alert = True
        else:
            # Reset variables
            start_time = None
            detected = False
            alert = False
    else:
        # Check if the average stayed at (or LESS than) threshold
        if average_ratio <= threshold:
            if start_time is None:
                # Initialize the timer
                start_time = time.time()
            elif time.time() - start_time >= duration and not detected:
                detected = True
                alert = True
        else:
            # Reset variables
            start_time = None
            detected = False
            alert = False

    # Return the updated variables
    return start_time, detected, alert

# Function to play alert
def alert_func(start_time, detected, alert, file1, file2, alert_count, alert_count_time):
    current_time = time.time()
    if detected and alert:
        if alert_count == 0:
	    # Start timing
            alert_count_time = current_time
            os.system(f"mpg321 -g 50 {file1}")
        elif alert_count == 1 and (current_time - alert_count_time) <= 300:
	    # Reset timing
            alert_count_time = current_time
            os.system(f"mpg321 -g 75 {file1}")
        elif (current_time - alert_count_time) <= 300:
	    # Reset timing
            alert_count_time = current_time
            os.system(f"mpg321 {file2}")
        else:
            # Reset alert count if more than 5 minutes passed
            alert_count = 0
            alert_count_time = current_time
            os.system(f"mpg321 -g 40 {file1}")
        # Increment alert count
        alert_count += 1
        # Reset variables
        start_time = None
        detected = False
        alert = False

    # Return the updated variables
    return start_time, detected, alert, alert_count, alert_count_time

# Main logic
def main():
    # Lists to store eye, turn and mouth ratios
    list_of_left_eye_ratios = []
    list_of_right_eye_ratios = []
    list_of_lips_ratios = []
    last_yaw_measurements = []

    # Open the video
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        exit()

    print("Press 'q' to quit.")

    # Audio file paths
    eyes_audio1 = "focus_on_the_road.mp3"
    eyes_audio2 = "Closed_eyes_detected_Stay_focused.mp3"
    yawn_audio1 = "consider_taking_a_break.mp3"
    yawn_audio2 = "Yawning_detected_Take_a_rest_soon.mp3"
    turn_audio1 = "Eyes_on_the_road.mp3"
    turn_audio2 = "You_looking_away_Please_focus_on_driving.mp3"

    # Default variables
    closed_start_time = yawn_start_time = turn_start_time = None
    sleepy_detected = yawn_detected = turn_detected = False
    closed_alert = yawn_alert = turn_alert = False
    eye_alert_count = yawn_alert_count = turn_alert_count = 0
    eye_alert_time = yawn_alert_time = turn_alert_time = None

    # Play system is on
    # os.system(f"mpg321 {file3}")

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

                # Call the detect_signs function to check if closed eyes are detected
                closed_start_time, sleepy_detected, closed_alert = detect_signs(average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, 24, 1)

                # Call the alert function
                closed_start_time, sleepy_detected, closed_alert, eye_alert_count, eye_alert_time = alert_func(closed_start_time, sleepy_detected, closed_alert, eyes_audio1, eyes_audio2, eye_alert_count, eye_alert_time)

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
                
                # Call the detect_signs function to check if yawn detected
                yawn_start_time, yawn_detected, yawn_alert = detect_signs(average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert, 30, 2)

                # Call the alert function
                yawn_start_time, yawn_detected, yawn_alert, yawn_alert_count, yawn_alert_time = alert_func(yawn_start_time, yawn_detected, yawn_alert, yawn_audio1, yawn_audio2, yawn_alert_count, yawn_alert_time)
                
                # Process face turn
                left_eyebrow = face_landmarks.landmark[105]
                right_eyebrow = face_landmarks.landmark[334]
                left_cheek = face_landmarks.landmark[234]
                right_cheek = face_landmarks.landmark[454]

                # Get the face turn aspect ratio
                face_turn_ratio = calculate_face_turn_ratio(left_eyebrow, right_eyebrow, left_cheek, right_cheek)
                last_yaw_measurements.append(face_turn_ratio)
                
                # Keeping only the last 3 measurements
                if len(last_yaw_measurements) > 3:
                    last_yaw_measurements.pop(0)
                
                # Calculate the average yaw
                averaged_yaw = sum(last_yaw_measurements) / len(last_yaw_measurements)
                
                # Call the detect_signs function to check if face turn detected
                turn_start_time, turn_detected, turn_alert = detect_signs(averaged_yaw, turn_start_time, turn_detected, turn_alert, 103, 3)

                # Call the alert function
                turn_start_time, turn_detected, turn_alert, turn_alert_count, turn_alert_time = alert_func(turn_start_time, turn_detected, turn_alert, turn_audio1, turn_audio2, turn_alert_count, turn_alert_time)

        # Break if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Play system is off
            # os.system(f"mpg321 {file4}")
            break

    # Release the video capture
    cap.release()
    face_mesh.close()

if __name__ == "__main__":
    main()
