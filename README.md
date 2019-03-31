# onlineChecker

This script pings a device on your network and reports this to Domoticz by setting a switch. Four arguments are required by the script:
`DEVICE`: the IP address or hostname of the device
`IDX`: the idx of the switch in Domoticz to set on or off
`INTERVAL`: the interval at which to check whether the device is online in seconds
`COOLDOWN`: the amount of seconds a device can be offline before it is actually reported to Domoticz
