#!/usr/bin/env python3
"""
Standlone test Test of timeseries ingestion

Test the Predix timeseries API, including integestion and query.

Depends on only websocket-client and requests. Runs as a command line utility. 

References
----------
See http://predix01.cloud.answerhub.com/questions/21920/time-series-3.html?childToView=21931#answer-21931
and https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=1549&tag=1613&journey=Exploring%20Security%20services&resources=1594,1593,2105,1544,1549,2255,1951

Copyright 2017 by Jeff Fischer
Licensed under the BSD 3-clause license.
"""

from websocket import create_connection
import sys
import logging
import json
import time
import requests
import argparse

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logging.basicConfig(level=logging.DEBUG)

INGEST_URL = 'wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages'
QUERY_URL='https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io/v1/datapoints'

import os
PIDSTR = str(os.getpid())

value_stream = [20, 21, 20, 19, 24]

def get_message_id():
    return PIDSTR + str(int(round(1000*time.time())))

def ts_to_predix_ts(ts):
    return int(round(1000*ts))

def create_ingest_body(sensor_id, ts, value):
    mid = get_message_id()
    datapoints = [[ts_to_predix_ts(ts), value],]
    return {'messageId':mid,
            'body': [{
                "name":str(sensor_id),
                "datapoints":datapoints,
                "attributes":{"test":True}
            }]}

def create_query_body(sensor_id, start_time, end_time):
    return {
        "cache_time": 0,
        "tags": [
            {
                "name": sensor_id,
                "order": "asc"
            }
        ],
        "start": ts_to_predix_ts(start_time),
        "end": ts_to_predix_ts(end_time)
    }


DESCRIPTION = \
"""End to end test of Predix Timeseries APIs.
Sends a sequence of data points via web sockets ingestion API and then
queries them back via the HTTPS query API."""

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--ingest-url", default=INGEST_URL,
                        help="Websockets URL for ingest. Default is for Western US datacenter")
    parser.add_argument("--query-url", default=QUERY_URL,
                        help="HTTPS URL for query. Default is for Western US datacenter")
    parser.add_argument("--sensor-id", default="sensor-1",
                        help="Sensor id (tag name) to use. Defaults to 'sensor-1'")
    parser.add_argument("predix_zone_id", metavar="PREDIX_ZONE_ID",
                        help="Zone Id for authentication")
    parser.add_argument("token_file", metavar="TOKEN_FILE",
                        help="Filename of a file containing the bearer token for authentication")
    parsed_args = parser.parse_args(args=argv)
    try:
        with open(parsed_args.token_file, 'r') as tf:
            token = tf.read().rstrip()
    except:
        parser.error("Problem opening/reading token file %s" % parsed_args.token_file)

    HEADERS = {'Predix-Zone-Id': parsed_args.predix_zone_id,
               'Authorization': 'Bearer ' + token,
               'Content-Type': 'application/json'}
        
    print("Connecting to %s..." % parsed_args.ingest_url)
    ws = create_connection(parsed_args.ingest_url, header=HEADERS)
    print("Connected")
    start_time = time.time()
    for value in value_stream:
        ts = time.time()
        print("sending value %d at time %s" % (value, ts))
        ws.send(json.dumps(create_ingest_body(parsed_args.sensor_id, ts, value)))
        result = ws.recv()
        print(result)
        time.sleep(1)
    end_time = time.time() + 1
    ws.close()

    # Sending query for data
    r = requests.post(QUERY_URL,
                      data=bytes(json.dumps(create_query_body('sensor-1',
                                                              start_time, end_time)),
                                 encoding='utf-8'),
                      headers=HEADERS)
    print(json.dumps(r.json(), indent=2))
    print("Test successful.")
    return 0


if __name__=="__main__":
    sys.exit(main())
