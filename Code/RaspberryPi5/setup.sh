#!/bin/bash
# Raspberry Pi setup

# Get update dependencies
sudo apt-get update

# Upgrading packages
sudo apt-get upgrade -y

# Performing distro upgrade
sudo apt-get dist-upgrade

# Updating firmware
sudo rpi-update

# Removing old packages
sudo apt autoremove -y

# Clearing cache
sudo apt autoclean

# Rebooting the system
sudo reboot

# Testing the speaker
speaker-test -D hw:0,0 -t sine -f 440 -c 2 -l 1

# Increasing the volume
alsamixer

# Press F6 to select a sound card.
# Use the arrow keys to navigate to your USB speaker and press Enter.
# Use the Up Arrow key to increase the volume.

# Save the setting
sudo alsactl store

# Testing the speaker again
speaker-test -D hw:0,0 -t sine -f 440 -c 2 -l 1

