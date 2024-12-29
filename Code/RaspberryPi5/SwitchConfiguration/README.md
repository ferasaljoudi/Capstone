
- The `switchTask.service` file is included in this directory. This file is required to run `switchTask.py` automatically when the Raspberry Pi starts. It ensures the script listens for the switch state.
- Create `switchTask.service` file:

```sh
sudo nano /etc/systemd/system/switchTask.service
```

- The lgpio library, which is used by RPi.GPIO, requires a temporary directory to create notification files for GPIO events.
- Create a `.lgpio` directory:

```sh
mkdir -p /home/safedrive/.lgpio
```

- Change the ownership of the directory is `safedrive`, since the service runs as `safedrive`:

```sh
chown safedrive:safedrive /home/safedrive/.lgpio
```

- Reloads the systemd manager configuration:

```sh
sudo systemctl daemon-reload
```

- Configures the service to start automatically at boot:

```sh
sudo systemctl enable switchTask.service
```

- Starts the service immediately:

```sh
sudo systemctl start switchTask.service
```

