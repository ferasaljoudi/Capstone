import os
import time
from collections import deque

import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Creating a double ended queue for plotting in real-time
yaw_data = deque(maxlen=100)
plt.ion()
fig, ax1 = plt.subplots()

# List to store the latest 3 yaw measurements
last_yaw_measurements = []

# Face turn ratio plot settings
line1, = ax1.plot([], [], lw=2, color='green')
ax1.set_ylim(70, 130)
ax1.set_xlim(0, 100)
ax1.set_xlabel("Frame")
ax1.set_ylabel("Yaw Angle (degrees)")
ax1.set_title("Turn Detection Monitoring")

# Open the video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

# Audio file path
file1 = "focus_on_the_road.mp3"

# Default variables
turn_start_time = None
turn_detected = False
turn_alert = False

# Function to calculate the face turn aspect ratio
def calculate_face_turn_ratio(left_eyebrow, right_eyebrow, left_cheek, right_cheek):
    # Calculate distances
    eyebrows_width = right_eyebrow.x - left_eyebrow.x
    face_width = right_cheek.x - left_cheek.x
    if face_width == 0:
        raise ValueError("Horizontal distance can not be zero.")
    # Return aspect ratio
    return (eyebrows_width / face_width) * 180

# Function to check if face turn is detected
def detect_face_turn(averaged_yaw, turn_start_time, turn_detected, turn_alert, threshold=103, duration=3):
    # Check the yaw average stayed at or below threshold for 3 seconds
    if averaged_yaw <= threshold:
        if turn_start_time is None:
            # Initialize the timer
            turn_start_time = time.time()
        elif time.time() - turn_start_time >= duration and not turn_detected:
            turn_detected = True
            turn_alert = True
    else:
        # Reset variables if the ratio falls below the threshold
        turn_start_time = None
        turn_detected = False
        turn_alert = False

    # Return the updated (turn_start_time, turn_detected, turn_alert)
    return turn_start_time, turn_detected, turn_alert

# Function to play face turn alert
def face_turn_alert_func(turn_start_time, turn_detected, turn_alert, file1):
    if turn_detected and turn_alert:
        # Play the turn_alert
        os.system(f"mpg321 {file1}")
        # Reset variables
        turn_start_time = None
        turn_detected = False
        turn_alert = False
    return turn_start_time, turn_detected, turn_alert

while True:
    success, frame = cap.read()
    if not success:
        print("Error: Can not read frame.")
        break

    # Convert frame to RGB since MediaPipe requires RGB input
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Extract key landmarks for detecting the face turn
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
            
            # Call the detect_face_turn function to check if face turn detected
            turn_start_time, turn_detected, turn_alert = detect_face_turn(averaged_yaw, turn_start_time, turn_detected, turn_alert)

            # Call the face turn alert function
            turn_start_time, turn_detected, turn_alert = face_turn_alert_func(turn_start_time, turn_detected, turn_alert, file1)

            # Update plot data
            yaw_data.append(averaged_yaw)
            line1.set_ydata(list(yaw_data))
            line1.set_xdata(range(len(yaw_data)))
            ax1.set_xlim(0, len(yaw_data))
            
            # Refresh the plot
            fig.canvas.draw()
            fig.canvas.flush_events()
    
    cv2.imshow("MediaPipe FaceMesh", frame)

    # Break if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the video capture and close the windows
cap.release()
cv2.destroyAllWindows()
plt.ioff()
plt.show()
