# onlineChecker

This script pings a device on your network and reports whether it is online or not to Domoticz by setting a virtual switch. In a wider context this can then be used to detect the presence of someone in your house.

## Installation

Navigate to your Domoticz' scripts folder (mine's `~/domoticz/scripts/`) and clone this repository into that directory:
`git clone https://github.com/jorijnsmit/onlineChecker.git`

onlineChecker depends on `requests` and could need `arping`:

`pip install requests`

`sudo apt-get install arping`

Edit the `credentials.py` file so that it contains your login detais for Domoticz.

You can now run the script! Four arguments are required by the script:

- `DEVICE`: the IP address or hostname of the device
- `IDX`: the idx of the switch in Domoticz to set on or off
- `INTERVAL`: the interval at which to check whether the device is online in seconds
- `COOLDOWN`: the amount of seconds a device can be offline before it is actually reported as such to Domoticz

So for example `python3 onlineChecker.py 192.168.1.1 1 5 300` would ping `192.168.1.1` every 5 seconds with a maximum cooldown of 300 seconds, switch Domoticz switch with idx `1` on or off accordingly.

## Run as a systemd service

The last step is then to install the script as a `systemd` service. This will make sure it always runs in the background, is restarted automatically, that it is started on reboot, it will log properly etc. You can learn more about it [here](https://wiki.debian.org/systemd).

A simple `.service` file to manage this script goes into `/etc/systemd/system/` and could like this:

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
Once that file is in place you can enable/disable, start/stop it etc. using `systemctl`.

That's all!

## Credits

All credits go to "Chopper_Rob" for the core logic of this script, as published on https://www.domoticz.com/wiki/Presence_detection.
