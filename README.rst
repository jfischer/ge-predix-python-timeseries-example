========================================
Predix Timeseries API Example for Python
========================================

This repo contains a standalone Python script to demonstrate the Predix Timeseries API. 

More details on configuration to be added shortly...

Usage
-----
Here are the command line arguments for the script::

    predix_timeseries_tester.py [-h] [--ingest-url INGEST_URL]
                                     [--query-url QUERY_URL]
                                     [--sensor-id SENSOR_ID]
                                     PREDIX_ZONE_ID TOKEN_FILE

    End to end test of Predix Timeseries APIs. Sends a sequence of data points via
    web sockets ingestion API and then queries them back via the HTTPS query API.

    positional arguments:
      PREDIX_ZONE_ID        Zone Id for authentication
      TOKEN_FILE            Filename of a file containing the bearer token for
                            authentication
    
    optional arguments:
      -h, --help            show this help message and exit
      --ingest-url INGEST_URL
                            Websockets URL for ingest. Default is for Western US
                            datacenter
      --query-url QUERY_URL
                            HTTPS URL for query. Default is for Western US
                            datacenter
      --sensor-id SENSOR_ID
                            Sensor id (tag name) to use. Defaults to 'sensor-1'

