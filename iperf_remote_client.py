#!/usr/bin/env python3
import sys
import json
import time
import requests
import iperf3
import config


'''
    To use:

        Configuration is done either by ENV Vars, or the config.py file
'''


################################################################################




while True:
    client = None
    result = None
    l = ""
    rq = None

    client = iperf3.Client()
    client.omit = int(config.IPERF3_OMIT)
    client.duration = config.IPERF3_DURATION
    client.server_hostname = config.IPERF3_SERVER
    client.port = config.IPERF3_PORT
    client.local_port = 5201
    
    print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
    result = client.run()

    if result.error:
        print(result.error)
    else:
        #print('')
        #print('Test completed:')
        #print('  started at         {0}'.format(result.time))
        #print('  bytes transmitted  {0}'.format(result.sent_bytes))
        #print('  retransmits        {0}'.format(result.retransmits))
        #print('  avg cpu load       {0}%\n'.format(result.local_cpu_total))
        #print('Average transmitted data in all sorts of networky formats:')
        #print('  bits per second      (bps)   {0}'.format(result.sent_bps))
        #print('  Kilobits per second  (kbps)  {0}'.format(result.sent_kbps))
        #print('  Megabits per second  (Mbps)  {0}'.format(result.sent_Mbps))
        #print('  KiloBytes per second (kB/s)  {0}'.format(result.sent_kB_s))
        #print('  MegaBytes per second (MB/s)  {0}'.format(result.sent_MB_s))

        #Build Influx Line Protocol
        l = "iperf"
        #l = l + ",lf=" + str(lf) + ",hf=" + str(hf) + " "
        l = l + ","
        l = l + "client" + "=" + result.local_host
        l = l + ","
        l = l + "server" + "=" + result.remote_host

        l = l + " " + "sent" + "=" + str(result.sent_bps)
        l = l + "," + "rcvd" + "=" + str(result.received_bps)
        #l = l + " " + str(time.time_ns())
        l = l + " " + str(result.timesecs * 1000000000)
        print(l)

        #Send to Grafana
        rq = requests.post("http://" + config.GRAFANA_SERVER + ":" + str(config.GRAFANA_PORT) + "/api/live/push/iperf", data=l, headers = {"Authorization": "Bearer " + config.GRAFANA_TOKEN})
        print(rq)

    print("Sleeping {0} seconds...".format(config.INTERVAL))
    time.sleep(config.INTERVAL)