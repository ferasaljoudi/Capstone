import os
import signal
import subprocess
import time

import RPi.GPIO as GPIO

# Pin configuration (GPIO17, physical pin number is 11)
SWITCH_PIN = 17

# GPIO setup
GPIO.setmode(GPIO.BCM)
# Internal pull-down resistor
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Variable to track process state
process = None

# Audio file paths
file1 = "detection_system_off.mp3"
file2 = "turn_on_reminder.mp3"

# Timer for playing file2
last_played = time.time()

try:
    while True:
        # If the switch is on
        if GPIO.input(SWITCH_PIN) == GPIO.HIGH:
            # Start the script if it's not already running
            if process is None:
                process = subprocess.Popen(
                    ['bash', '-c', 'source ../../capstone/bin/activate && python eye_detection_mediapipe.py'],
                    cwd='/home/safedrive/capstone/eye_detection',
                    # Start a new process group
                    preexec_fn=os.setsid
                )
        else:
            # Stop the script if it's running
            if process is not None:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                process = None
                # Play system is off
                os.system(f"mpg321 {file1}")
            
            # Play a reminder every 10 minutes
            if time.time() - last_played >= 600:
                os.system(f"mpg321 {file2}")
                # Reset the timer
                last_played = time.time()
        # Noise delay
        time.sleep(0.1)

except KeyboardInterrupt:
    if process is not None:
        # Clean up process
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
finally:
    GPIO.cleanup()
