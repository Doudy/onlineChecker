# onlineChecker

This script pings a device on your network and reports whether it is online or not to Domoticz by setting a switch. Four arguments are required by the script:

- `DEVICE`: the IP address or hostname of the device
- `IDX`: the idx of the switch in Domoticz to set on or off
- `INTERVAL`: the interval at which to check whether the device is online in seconds
- `COOLDOWN`: the amount of seconds a device can be offline before it is actually reported as such to Domoticz

All credits go to "Chopper_Rob" for the core logic of this script, as published on https://www.domoticz.com/wiki/Presence_detection.

What I did in this version is to upgrade it from Python 2 to Python 3.6+ and make it suitable to be run as a `systemd` service. By running it as such as service the script becomes more compact and stable at the same time.

A simple `.service` file to manage this script would go into `/etc/systemd/system/` and could like this:

```
[Unit]
Description=onlineChecker

[Service]
Type=simple
ExecStart=/usr/bin/python3 -u onlineChecker.py 192.168.1.1 1 5 300
WorkingDirectory=/home/jorijnsmit/domoticz/scripts/onlineChecker
User=jorijnsmit
Restart=always

[Install]
WantedBy=multi-user.target
```
You can then enable/disable it, start/stop etc. using [`systemctl`](https://www.freedesktop.org/software/systemd/man/systemctl.html).
