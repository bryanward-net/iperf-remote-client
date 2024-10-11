#!/usr/bin/env python3
import sys
import json
import time
import requests

import config


'''
    To use:
        Run `iperf3 --json -c 1.2.3.4` from the command line and pipe the output into this script.
        Example:
            iperf3 --json -c 1.2.3.4 | ./iperf_remote_parser.py
        Example to run a 1-second test every 3 seconds:
            watch -n3 "iperf3 -c iperf.example.com --json -i 1 -t 1 | ./iperf_remote_parser.py"

        Configuration is done either by ENV Vars, or the config.py file
'''


################################################################################

json_in = ""

for line in sys.stdin:
    #print(line)
    #print("-----")
    if line is not None:
        json_in = json_in + line
    else:
        break
    #Else, done getting data

j = json.loads(json_in)

#Build Influx Line Protocol
l = "iperf"
#l = l + ",lf=" + str(lf) + ",hf=" + str(hf) + " "
l = l + ","
l = l + "client" + "=" + j['start']['connected'][0]['local_host']
l = l + ","
l = l + "server" + "=" + j['start']['connected'][0]['remote_host']

l = l + " " + "sent" + "=" + str(j['end']['sum_sent']['bits_per_second'])
l = l + "," + "rcvd" + "=" + str(j['end']['sum_received']['bits_per_second'])
#l = l + " " + str(time.time_ns())
l = l + " " + str(j['start']['timestamp']['timesecs'] * 1000000000)
print(l)

#Send to Grafana
rq = requests.post("http://" + config.GRAFANA_SERVER + ":" + config.GRAFANA_PORT + "/api/live/push/iperf", data=l, headers = {"Authorization": "Bearer " + config.GRAFANA_TOKEN})
print(rq)
