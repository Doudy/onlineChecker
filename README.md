# onlineChecker

This script pings a device on your network and reports whether it is online or not to Domoticz by setting a virtual switch. In a wider context this can then be used to detect the presence of someone or some activity in your house (e.g. am I home, is the laptop or tv on, etc.)

## Installation

Navigate to your Domoticz' scripts folder (mine's `~/domoticz/scripts/`) and clone this repository into that directory:
`git clone https://github.com/jorijnsmit/onlineChecker.git`

onlineChecker depends on the [`requests` library](http://docs.python-requests.org/en/master/):

`pip install requests`

Copy or rename `credentials.py.template` to `credentials.py` and edit the file so that it contains your Domoticz and device details.

You can now run the script!

## Run as a systemd service

To help manage when and how the script runs, you can install it as a `systemd` service. This will make it very easy to always run in the background, have it restart automatically, have it run on startup, it will log properly etc. You can learn more about systemd [here](https://wiki.debian.org/systemd).

A simple `.service` file to manage this script goes into `/etc/systemd/system/` and could like this:

```
[Unit]
Description=onlineChecker

[Service]
Type=simple
ExecStart=/usr/bin/python3 -u onlineChecker.py
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
