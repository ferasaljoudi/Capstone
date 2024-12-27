import os

# File paths
file_paths = [
    "focus_on_the_road.mp3",
    "consider_taking_a_rest.mp3",
    "detection_system_on.mp3",
    "detection_system_off.mp3"
]

# Play each file
for file_path in file_paths:
    os.system(f"mpg321 {file_path}")
    print(f"Played: {file_path}")
