# iperf-remote-client

Docker image to run iperf and publish data to a Grafana Live or InfluxDB server


## Pre-Requisites

iperf3 binaries and libiperf (included with iperf3)
Python 3
`pip3 install iperf3 requests`

## Getting started

Copy config.skel to config.py and fill out the variables.
Or, set environment variables, which will take precedence over those set in config.py

### iperf_remote_parser.py
To use:
    Run `iperf3 --json -c 1.2.3.4` from the command line and pipe the output into this script.

    Example:
        iperf3 --json -c 1.2.3.4 | ./iperf_remote_parser.py

    Example to run a 1-second test every 3 seconds:
        watch -n3 "iperf3 -c iperf.example.com --json -i 1 -t 1 | ./iperf_remote_parser.py"

### iperf_remote_client.py
Does not require the use of a a shell or a pipe.  This script runs the test as well as publishes the results.
To use:
    Run `./iperf_remote_client.py`.  All config is done via config.py or environment variables.