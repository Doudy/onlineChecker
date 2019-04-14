import subprocess
import datetime
import time

import requests

try:
    from credentials import *
except ModuleNotFoundError:
    raise Exception('Copy/rename credentials.py.template to credentials.py and edit it with your own details.')

IDX = str(IDX)
DOMO_URL = 'http://'+DOMO_SERVER+'/json.htm?'

def domoRequest(req):
    try:
        r = requests.get(DOMO_URL+req, auth=(DOMO_USER, DOMO_PASS))
    except requests.exceptions.ConnectionError:
        raise Exception('Could not connect to '+DOMO_SERVER+'.')
    if r.ok:
        return r.json()
    raise Exception('Could not connect to Domoticz (status code '+r.status_code+'.')

def domoCommand(cmd):
    print(domoRequest('type=command&param=switchlight&idx='+IDX+'&switchcmd='+cmd+'&passcode='+DOMO_PROTECTION)['status'])

def domoStatus():
    response = domoRequest('type=devices&rid='+IDX)

    if 'result' in response:
        try:
            status = response['result'][0]['Status']
        except:
            raise Exception('Unknown response '+response['result']+'.')
        if status == 'On':
            return True
        if status == 'Off':
            return False
        raise Exception('Switch with idx '+IDX+' has unknown status ("'+status+'").')
    raise Exception('Switch with idx '+IDX+' does not exist.')

def infiniteLoop():
    wasOnline = None
    lastReported = None
    lastSeen = datetime.datetime.now()

    while True:
        pingReply = subprocess.call('ping -q -c1 -W 1 '+DEVICE+' > /dev/null', shell=True)
        isOnline = bool(pingReply == 0)

        if isOnline:
            lastSeen = datetime.datetime.now()
            if isOnline != wasOnline:
                if lastReported:
                    print(DEVICE+' came back online, no need to tell Domoticz.')
                else:
                    if domoStatus():
                        print(DEVICE+' is online, but Domoticz already knew.')
                    else:
                        print(DEVICE+' came online, telling Domoticz it\'s back.')
                        domoCommand('On')
                    lastReported = True
        else:
            if isOnline != wasOnline:
                print(DEVICE+' went offline, waiting for it to come back...')
            if (datetime.datetime.now() - lastSeen).total_seconds() > COOLDOWN and not lastReported:
                if domoStatus():
                    print(DEVICE+' went offline, telling Domoticz it\'s gone.')
                    domoCommand('Off')
                else:
                    print(DEVICE+' is offline, but Domoticz already knew.')
                lastReported = False

        wasOnline = isOnline
        time.sleep(INTERVAL)

infiniteLoop()
