import sys
import subprocess
import datetime
import time
import requests

from credentials import *

if len(sys.argv) != 5:
    raise Exception('Script requires four arguments: DEVICE IDX INTERVAL COOLDOWN')

DEVICE = sys.argv[1]
IDX = sys.argv[2]
INTERVAL = float(sys.argv[3])
COOLDOWN = float(sys.argv[4])

DOMO_URL = f'http://{DOMO_SERVER}/json.htm?'

def domoRequest(req):
    return requests.get(DOMO_URL + req, auth=(DOMO_USER, DOMO_PASS)).json()

def domoCommand(cmd):
    print(domoRequest(f'type=command&param=switchlight&idx={IDX}&switchcmd={cmd}')['status'])

def domoStatus():
    response = domoRequest(f'type=devices&rid={IDX}')

    if 'result' in response:
        status = response['result'][0]['Status']
        if status == 'On':
            return True
        if status == 'Off':
            return False
        raise Exception(f'Switch with idx {IDX} has unknown status ("{status}").')
    raise Exception(f'Switch with idx {IDX} does not exist.')

def infiniteLoop():
    previousReply = -1
    lastReported = -1
    lastSeen = datetime.datetime.now()

    while True:
        pingReply = subprocess.call(f'ping -q -c1 -W 1 {DEVICE} > /dev/null', shell=True)

        if pingReply == 0: # 0 means device is online!
            lastSeen = datetime.datetime.now()
            if pingReply != previousReply:
                if lastReported == 1:
                    print(f'{DEVICE} came back online, no need to tell Domoticz.')
                else:
                    if domoStatus():
                        print(f'{DEVICE} is online, but Domoticz already knew.')
                    else:
                        print(f'{DEVICE} came online, telling Domoticz it\'s back.')
                        domoCommand('On')
                    lastReported = 1

        if pingReply != 0: # device is offline or responds too slow
            if pingReply != previousReply:
                print(f'{DEVICE} went offline, waiting for it to come back...')
            if (datetime.datetime.now() - lastSeen).total_seconds() > COOLDOWN and lastReported != 0:
                if domoStatus():
                    print(f'{DEVICE} went offline, telling Domoticz it\'s gone.')
                    domoCommand('Off')
                else:
                    print(f'{DEVICE} is offline, but Domoticz already knew.')
                lastReported = 0

        time.sleep(INTERVAL)
        previousReply = pingReply

infiniteLoop()
