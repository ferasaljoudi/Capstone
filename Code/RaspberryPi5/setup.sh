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