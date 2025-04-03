#!/bin/bash
# Raspberry Pi setup

# Connect to the Raspberry Pi via SSH
ssh safedrive@ifs.local

# Update the package lists
sudo apt update

# Perform a full system upgrade
sudo apt full-upgrade -y

# Remove unnecessary packages
sudo apt autoremove -y

# Clean the local repository from retrieved package files
sudo apt clean

# Rebooting the system
sudo reboot

# Testing the speaker
speaker-test -D hw:2,0 -t sine -f 440 -c 2 -l 1

# Increasing the volume
alsamixer

# Press F6 to select a sound card.
# Use the arrow keys to navigate to your USB speaker and press Enter.
# Use the Up Arrow key to increase the volume. (We set it to 60/100)

# Save the setting
sudo alsactl store

# Testing the speaker again
speaker-test -D hw:2,0 -t sine -f 440 -c 2 -l 1

# Testing the camera:
# Connect the camera to the RPi and reboot
sudo shutdown -r now

libcamera-hello # Test the camera

# Install OpenCV for Python
sudo apt install python3-opencv -y

# Create a Python virtual environment
python3 -m venv capstone
# Activate the environment
source capstone/bin/activate

# Install dependencies
pip install opencv-python
pip install mediapipe
Pip install cvzone
pip install opencv-python tensorflow
# Audio dependencies
pip install gTTS
sudo apt install mpg321

# Create a directory and navigate to it
mkdir capstone/eye_detection
cd capstone/eye_detection

# Create python script and run it
nano eye_detection_tflite.py
python eye_detection_tflite.py

# To deactivate the environment
deactivate

# Below is the steps for setting up the GPS module and testing it

# Open the Raspberry Pi configuration tool
sudo raspi-config

# Navigate to Interfacing Options
# Select Serial Port
# Enable the serial port hardware
# Exit and reboot
sudo reboot

# Find the port which the GPS connected to
dmesg | grep tty # For our system it was ttyACM0

# Read GPS data to check if the module is outputting something
cat /dev/ttyACM0

# Test getting the location
head -n 20 /dev/ttyACM0 | grep GPGGA

# Test getting the speed
head -n 20 /dev/ttyACM0 | grep GPVTG

# Additional set up for adding a beep sound
# New terminal
sudo apt install numpy sounddevice
source capstone/bin/activate
cd capstone/eye_detection/
pip install sounddevice
