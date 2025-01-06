<div align="center">

# Raspberry Pi: Setup, Configuration, and Scripts

</div>

Below is a description of the contents in this directory, outlining the setup and configurations performed entirely on the Raspberry Pi:

### `setup.sh`

- This script sets up the Raspberry Pi environment, including system updates, audio configuration, and testing peripherals like the speaker and camera.
- It ensures the system is updated, cleaned, and rebooted for optimal performance.
- Prepares a Python environment with all dependencies and tools for Python development, including OpenCV, MediaPipe, TensorFlow, and gTTS, within a virtual environment.

### CreatingAudioFiles Directory

- This directory has the created audio files, a file to create them and a file to play them.
- The gTTS (Google Text-to-Speech) library was used to create audio files by converting text into speech. Each file was saved as an MP3 using `gTTS`. For playing the audio files, we used the `os.system` command with the `mpg321` utility.

### SpeakerConfiguration Directory

- This directory contains files and configurations to ensure the speaker settings persist across reboots on the Raspberry Pi.
- The `asound.conf` file sets the default sound card for consistent audio playback.
- The `rc.local` file and its associated service ensure volume levels, are restored automatically during system boot.
- These configurations were necessary because ALSA settings revert to default after a reboot without them.

### SwitchConfiguration Directory

- This directory contains configurations to enable or disable the detection system via a switch when the Raspberry Pi powers on, ensuring hands-free operation.
- The `switchTask.service` file ensures the `switchTask.py` script starts automatically at boot and listens for the switch state.
- The `.lgpio` directory is set up to support GPIO event notifications required by the `lgpio` library, with proper ownership for seamless operation.
- These configurations automate the system's response to the switch state, making the setup reliable and user-friendly.

### `eye_detection_tflite.py` And `tflite_visual.py`

- The detection in these files are done as below:
    - TFlite model to detect the closed eyes.
    - MediaPipe to detect the yawn.
- These two files do the same detection and alert tasks in the same way.
- The `tflite_visual.py` file include the extra visual display which was used to test and view the result in the development stage.
- The `eye_detection_tflite.py` file is the final script ready to be used without a display.

### `eye_detection_mediapipe.py` And `mediapipe _visual.py`

- The detection in these files are done using MediaPipe to detect both closed eyes and yawn.
- These two files do the same detection and alert tasks in the same way.
- The `mediapipe _visual.py` file include the extra visual display which was used to test and view the result in the development stage.
- The `eye_detection_mediapipe.py` file is the final script ready to be used without a display.
