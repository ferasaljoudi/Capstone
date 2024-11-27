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
