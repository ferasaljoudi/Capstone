from gtts import gTTS

# Text to be spoken
texts = [
    "Please focus on the road",
    "Closed eyes detected! Stay focused",
    "Consider taking a break",
    "Yawning detected! Take a rest soon",
    "Eyes on the road!",
    "You’re looking away! Please focus on driving",
    "The detection system is on",
    "The detection system is in auto mode",
    "Do not forget to turn on the detection system",
    "Auto detection is off, consider turning it on manually"
]

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

# Create and save audio files
for text, file_path in zip(texts, file_paths):
    tts = gTTS(text=text, lang='en')
    tts.save(file_path)
    print(f"Created: {file_path}")