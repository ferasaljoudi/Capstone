import os
import signal
import subprocess
import time

import RPi.GPIO as GPIO
import serial

# Pin configuration (GPIO17, physical pin number is 11)
SWITCH_PIN = 17

# GPIO setup
GPIO.setmode(GPIO.BCM)
# Internal pull-down resistor
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Open the GPS serial port
try:
    gps_port = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
except serial.SerialException:
    gps_port = None

# Variable to track process state
process = None

# Audio file paths
file0 = "detection_system_on.mp3"
file1 = "detection_system_off.mp3"
file2 = "turn_on_reminder.mp3"
file3 = "speed_over_20km.mp3"
file4 = "speed_below_20km.mp3"

# Timer for playing file2
last_played = time.time()

try:
    while True:
        # Read a line of data from the GPS module
        if gps_port is not None:
            try:
                line = gps_port.readline().decode('ascii', errors='ignore')
            except serial.SerialException:
                line = ""

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
                os.system(f"mpg321 {file0}")
        # Check for the line that contains the GPVTG sentence (it contains speed)
        elif line and line.startswith('$GPVTG'):
            parts = line.split(',')
            # Extract the speed in km/h (field index 7 in GPVTG)
            if len(parts) > 7 and parts[7]:
                try:
                    speed_kmh = float(parts[7])
                    last_played = time.time()

                    if speed_kmh > 20:
                        if process is None:
                            process = subprocess.Popen(
                                ['bash', '-c', 'source ../../capstone/bin/activate && python eye_detection_mediapipe.py'],
                                cwd='/home/safedrive/capstone/eye_detection',
                                preexec_fn=os.setsid
                            )
                    elif speed_kmh <= 20:
                        if process is not None:
                            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                            process = None
                except ValueError:
                    pass
        else:
            # Stop the script if it's running
            if process is not None:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                process = None
                # Play system is off
                os.system(f"mpg321 {file1}")
                last_played = time.time()
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