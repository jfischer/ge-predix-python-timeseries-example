========================================
Predix Timeseries API Example for Python
========================================

This repo contains a standalone Python script to demonstrate the Predix Timeseries API.
The script connects via websockets and sends five ingest messages with a single
sensor value each. It then makes an HTTP request to query back the sensor values.

Predix Configuration Hints
--------------------------
Before running the script, you will need to configure on Predix a UAA (User
Authentication and Authorization) service and a Timeseries service. I found the
following Predix tutorials helpful:

1. `Build a basic application: Introduction and Installer <https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=1580>`_.
   You should not need the Java dependencies (JDK and Maven), since we are using
   Python instead.
2. `Exploring Application Security: Configure UAA for user authentication <https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=1544>`_.
   Rather than use the ``cf login`` command, I found it easier to use the
   Predix CLI's ``px login`` command instead. It is a more
   user-friendly wrapper over the Cloud Foundry login that prompts you for the
   region, username, and password rather than requiring that you figure out the
   endpoint yourself.
3. `Exploring Application Security: Create a Predix Service and set up a UAA ClientId <https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=1549>`_.
   It appears that you need to have a Cloud Foundry application pushed up to Predix
   and configured with permissions to the Time Series service, even though we
   will not be using the actual application. The step
   "Find the application to bind to" describes how to push up the
   ``predix-nodejs-starter`` application, which will satisfy this requirement.
   One other comment: be sure to to add the zone token scopes, as described in
   step 9.
4. `Exploring Time Series: Introduction to the Time Series API <https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=1556>`_.
   You can get your Predix Zone Id by running the ``px service-info`` comand.
   The Zone Id is the value of the field ``zone-http-header-value``. I highly
   recommend testing the Timeseries API via the Predix Toolkit web UI before
   running the Python script.[#f1]_

.. [#f1] Update: I ran into an issue with the Zone Id returned by ``px service info``.
         Apparently, the token had expired and the Zone Id was no longer valid.
         I was unable to get the token to be renewed from the Command Line
         Interface. I was able to get things working by extracting the Zone Id from
         the scope names, as described in
         `this <http://forum.predix.io/questions/3290/timeseries-401-unauthorized.html>`__
         Predix Forum question (see the response by Beth).

Python Dependencies
-------------------
The script is for Python 3, so you will need a Python 3 install, version 3.4 or
later. You will also need the ``websocket-client`` and ``requests`` packages.
You can install them via pip as follows::

  pip3 install websocket-client requests


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


At a minimum, you will need the Predix Zone Id (obtainable via
``px service-info`` and the bearer token. You can get the token
via the `Predix Toolkit <https://predix-toolkit.run.aws-usw02-pr.ice.predix.io>`_:

1. Select "Client ID Login" from the left sidebar
2. Enter your instance URL, client id, and client secret. Note that, if you
   are not currently logged in, the instance URL is populated with an invalid
   value. You can get the instance URL from the Predix console or through
   ``cf env`` (use the value of the ``uri`` property within ``predix-uaa``).
3. When you click on the "Submit" button, the page should be updated with a
   JSON object containing properties ``access_token``, ``token_type``,
   ``expires_in``, ``scope``, and ``jti``. The token file provided to
   the test script should contain the *value* of the ``access_token``
   property.
  
The default ingest URL and query URL are fine if you are using the Western
US Predix data center. Otherwise, you can override them with the values for the
data center you are using (they are available through ``px service-info`` as well
as through the Predix Toolkit).

Example Execution
-----------------
Here is an example terminal session showing the script being
run and its output::

    $ python predix_timeseries_tester.py 2ca08954-dcb1-4f20-b3a8-84cd60dd5608 token.txt
    Connecting to wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages...
    Connected
    sending value 20 at time 1496198975.454793
    {"statusCode":202,"messageId":"65271496198975455"}
    sending value 21 at time 1496198976.596692
    {"statusCode":202,"messageId":"65271496198976597"}
    sending value 20 at time 1496198977.734978
    {"statusCode":202,"messageId":"65271496198977735"}
    sending value 19 at time 1496198978.873025
    {"statusCode":202,"messageId":"65271496198978873"}
    sending value 24 at time 1496198980.013747
    {"statusCode":202,"messageId":"65271496198980014"}
    Starting new HTTPS connection (1): time-series-store-predix.run.aws-usw02-pr.ice.predix.io
    https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io:443 "POST /v1/datapoints HTTP/1.1" 200 257
    {
      "tags": [
        {
          "name": "sensor-1",
          "results": [
            {
              "values": [
                [
                  1496198975455,
                  20,
                  3
                ],
                [
                  1496198976597,
                  21,
                  3
                ],
                [
                  1496198977735,
                  20,
                  3
                ],
                [
                  1496198978873,
                  19,
                  3
                ],
                [
                  1496198980014,
                  24,
                  3
                ]
              ],
              "attributes": {
                "test": [
                  "true"
                ]
              },
              "groups": [
                {
                  "name": "type",
                  "type": "number"
                }
              ]
            }
          ],
          "stats": {
            "rawCount": 5
          }
        }
      ]
    }
    Test successful.  


Copyright 2017 by Jeff Fischer.
