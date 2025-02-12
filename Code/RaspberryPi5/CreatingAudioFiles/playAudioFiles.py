import os

# File paths
file_paths = [
    "focus_on_the_road.mp3",
    "Closed_eyes_detected_Stay_focused.mp3",
    "consider_taking_a_break.mp3",
    "Yawning_detected_Take_a_rest_soon.mp3",
    "Eyes_on_the_road.mp3",
    "You_looking_away_Please_focus_on_driving.mp3",
    "detection_system_on.mp3",
    "detection_system_in_auto_mode.mp3",
    "turn_on_reminder.mp3",
    "auto_off_reminder.mp3"
]

# Play each file
for file_path in file_paths:
    # The below line play the files at default -g 100
    os.system(f"mpg321 {file_path}")
    # The below two lines play the files at lower volume
    # os.system(f"mpg321 -g 40 {file_path}")
    # os.system(f"mpg321 -g 70 {file_path}")
    print(f"Played: {file_path}")
    