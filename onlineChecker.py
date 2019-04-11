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
    print(domoRequest('type=command&param=switchlight&idx='+IDX+'&switchcmd='+cmd)['status'])

def domoStatus():
    response = domoRequest('type=devices&rid='+IDX)

    if 'result' in response:
        status = response['result'][0]['Status']
        if status == 'On':
            return True
        if status == 'Off':
            return False
        raise Exception('Switch with idx '+IDX+' has unknown status ("'+status+'").')
    raise Exception('Switch with idx '+IDX+' does not exist.')

def infiniteLoop():
    previousReply = -1
    lastReported = -1
    lastSeen = datetime.datetime.now()

    while True:
        pingReply = subprocess.call('ping -q -c1 -W 1 '+DEVICE+' > /dev/null', shell=True)

        if pingReply == 0: # 0 means device is online!
            lastSeen = datetime.datetime.now()
            if pingReply != previousReply:
                if lastReported == 1:
                    print(DEVICE+' came back online, no need to tell Domoticz.')
                else:
                    if domoStatus():
                        print(DEVICE+' is online, but Domoticz already knew.')
                    else:
                        print(DEVICE+' came online, telling Domoticz it\'s back.')
                        domoCommand('On')
                    lastReported = 1

        if pingReply != 0: # device is offline or responds too slow
            if pingReply != previousReply:
                print(DEVICE+' went offline, waiting for it to come back...')
            if (datetime.datetime.now() - lastSeen).total_seconds() > COOLDOWN and lastReported != 0:
                if domoStatus():
                    print(DEVICE+' went offline, telling Domoticz it\'s gone.')
                    domoCommand('Off')
                else:
                    print(DEVICE+' is offline, but Domoticz already knew.')
                lastReported = 0

        time.sleep(INTERVAL)
        previousReply = pingReply

infiniteLoop()
