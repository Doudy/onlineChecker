# domoticz login details
DOMO_SERVER = 'localhost:8080'  # the IP address or hostname of the device
DOMO_USER = 'username'
DOMO_PASS = 'password'

# device we want to ping
DEVICE = '0.0.0.0'  # the IP address or hostname of the device
IDX = 99  # the idx of the switch in Domoticz to set on or off
INTERVAL = 5  # the interval at which to check whether the device is online in seconds
COOLDOWN = 300  # the amount of seconds a device can be offline before it is actually reported as such to Domoticz
