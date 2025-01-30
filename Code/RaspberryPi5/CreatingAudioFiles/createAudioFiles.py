from gtts import gTTS

# Text to be spoken
texts = [
    "Please focus on the road",
    "Consider taking a rest",
    "The detection system is on",
    "The detection system is off",
    "Do not forget to turn on the detection system",
    "Your speed is over 20 Km/h",
    "Your speed is below 20 Km/h",
    "Auto detection is off, consider turning it on manually"
]

# File paths
file_paths = [
    "focus_on_the_road.mp3",
    "consider_taking_a_rest.mp3",
    "detection_system_on.mp3",
    "detection_system_off.mp3",
    "turn_on_reminder.mp3",
    "speed_over_20km.mp3",
    "speed_below_20km.mp3",
    "auto_off_reminder.mp3"
]

# Create and save audio files
for text, file_path in zip(texts, file_paths):
    tts = gTTS(text=text, lang='en')
    tts.save(file_path)
    print(f"Created: {file_path}")
