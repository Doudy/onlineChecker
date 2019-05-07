#!/usr/bin/python

import sys
import subprocess
import datetime
import time
from configparser import ConfigParser

import requests

FILENAME = sys.argv[1] if len(sys.argv) > 1 else 'config.ini'
CONFIG = ConfigParser()
CONFIG.read(FILENAME)
try:
    DOMO = CONFIG['DOMOTICZ']
    DEVICE = CONFIG['DEVICE']
except (KeyError, TypeError):
    raise Exception('Config file is unreadable or incomplete.')
DOMO['URL'] = 'http://'+DOMO['SERVER']+'/json.htm?'

def domo_request(req):
    try:
        r = requests.get(DOMO['URL']+req, auth=(DOMO['USER'], DOMO['PASS']))
    except requests.exceptions.ConnectionError:
        raise Exception('Could not connect to '+DOMO['SERVER']+'.')
    if r.ok:
        return r.json()
    raise Exception('Could not connect to Domoticz (status code '+r.status_code+'.')

def domo_command(cmd):
    print(domo_request('type=command&param=switchlight&idx='\
    +DEVICE['IDX']+'&switchcmd='+cmd+'&passcode='+DOMO['PROTECTION'])['status'])

def domo_status():
    response = domo_request('type=devices&rid='+DEVICE['IDX'])

    if 'result' in response:
        try:
            status = response['result'][0]['Status']
        except:
            raise Exception('Unknown response '+response['result']+'.')
        if status == 'On':
            return True
        if status == 'Off':
            return False
        raise Exception('Switch with idx '+DEVICE['IDX']+' has unknown status ("'+status+'").')
    raise Exception('Switch with idx '+DEVICE['IDX']+' does not exist.')

def ping_device(ip=DEVICE['IP']):
    ping_reply = subprocess.call('ping -q -c1 -W 1 '+ip+' > /dev/null', shell=True)
    return bool(ping_reply == 0)

def infinite_loop():
    was_online = None
    last_reported = None
    last_seen = datetime.datetime.now()

    while True:
        is_online = ping_device()

        if is_online:
            last_seen = datetime.datetime.now()
            if is_online != was_online:
                if last_reported:
                    print(DEVICE['IP']+' came back online, no need to tell Domoticz.')
                else:
                    if domo_status():
                        print(DEVICE['IP']+' is online, but Domoticz already knew.')
                    else:
                        print(DEVICE['IP']+' came online, telling Domoticz it\'s back.')
                        domo_command('On')
                    last_reported = True
        else:
            if is_online != was_online:
                print(DEVICE['IP']+' went offline, waiting for it to come back...')
            if (datetime.datetime.now() - last_seen).total_seconds() > DEVICE.getint('COOLDOWN')\
            and not last_reported:
                if domo_status():
                    print(DEVICE['IP']+' went offline, telling Domoticz it\'s gone.')
                    domo_command('Off')
                else:
                    print(DEVICE['IP']+' is offline, but Domoticz already knew.')
                last_reported = False

        was_online = is_online
        time.sleep(DEVICE.getint('INTERVAL'))

infinite_loop()
