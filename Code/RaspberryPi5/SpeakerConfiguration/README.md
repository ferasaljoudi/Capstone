Editing the speaker volume using `alsamixer` will work fine in the current session. However, if the RPi rebooted, the volume will be back to its default. This is why we needed to make the below configurations.

###  Identify the Working Sound Card

- Increasing the volume and save the setting:

```sh
alsamixer
sudo alsactl store
```

- List all available sounds cards using `aplay -l`, and test them one by one using `speaker-test` to identify the card that works. The one worked for our case was `hw:1,0`.

### Set the Default Sound Card

- The `asound.conf` file is included in this directory. Replace 1 with the working card number. This file sets the default sound card so the Raspberry Pi knows which audio device to use for playback.
- Create the ALSA configuration file:

```sh
sudo nano /etc/asound.conf
```

- Save the current ALSA setting:

```sh
sudo alsactl store
```

### Ensure Settings Restore on Boot

- The `rc.local` file is included in this directory. This file ensures that ALSA settings (like volume levels) are restored automatically during system boot.
- Create `rc.local` file:

```sh
sudo nano /etc/rc.local
```

- Make the file executable:

```sh
sudo chmod +x /etc/rc.local
```

### Create and Enable the rc-local Service

- The `rc-local.service` file is included in this directory. This file enables compatibility for the rc.local script with systemd, allowing it to run at startup.
- Create `rc-local.service` file:

```sh
sudo nano /etc/systemd/system/rc-local.service
```

- Reloads the systemd manager configuration:

```sh
sudo systemctl daemon-reload
```

- Configures the service to start automatically at boot:

```sh
sudo systemctl enable rc-local
```

- Starts the service immediately:

```sh
sudo systemctl start rc-local
```

- Test and verify:

```sh
sudo reboot
speaker-test -c2 -twav
```