#!/usr/bin/python3

import holyromanpv
import time
import os

home = os.path.expanduser("~")
config_loc = home + '/holyromanpv/data/config.ini'
config_file = holyromanpv.config.get_config(config_loc)

ip = config_file['smartplug']['ip']
port = int(config_file['smartplug']['port'])

interface = holyromanpv.Interface(ip=ip, port=port)

while True:
    df = interface.get_realtime()
    ts = df.timestamp.values[0][0:-13]
    power = round(df.power.values[0]*10)/10
    print('{ts}  {power} Watt'.format(ts=ts, power=power))
    time.sleep(5)
