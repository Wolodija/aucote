Port scans
==========

List
----

Obtains list of port scans from Aucote's storage. Port scan is a connection between port and scan.
Single port scan provides information about timestamp of scan of specific port.

URL
~~~

.. code::

    /api/v1/ports?limit=<limit>&page=<page>

Parameters limit and offset are optional. Limit defines how many rows should be returned 
and page defines page of results. First page has number 0.

For parameters ``limit=10``, ``offset=3`` the rows from 30 to 39 will be displayed.

Request
~~~~~~~

.. code::

    curl "http://localhost:1235/api/v1/ports?limit=2&page=13"

Response
~~~~~~~~

.. code-block:: json

    {
      "ports": [
        {
          "id": 5148,
          "url": "http://localhost:1235/api/v1/ports/5148",
          "port": {
            "port_number": 21,
            "protocol": "TCP",
            "node": "10.12.1.159[315]"
          },
          "timestamp": 1508844360.607725,
          "timestamp_human": "2017-10-24T11:26:00.607725+00:00",
          "scan": "tools_advanced"
        },
        {
          "id": 5147,
          "url": "http://localhost:1235/api/v1/ports/5147",
          "port": {
            "port_number": 3268,
            "protocol": "TCP",
            "node": "10.12.2.175[315]"
          },
          "timestamp": 1508844360.6077192,
          "timestamp_human": "2017-10-24T11:26:00.607719+00:00",
          "scan": "tools_advanced"
        }
      ],
      "navigation": {
        "limit": 2,
        "page": 13,
        "next_page": "http://localhost:1235/api/v1/ports?limit=2&page=14",
        "previous_page": "http://localhost:1235/api/v1/ports?limit=2&page=12"
      },
      "meta": {
        "timestamp": 1508848237.9150612,
        "human_timestamp": "2017-10-24T12:30:37.915061+00:00"
      }
    }

The most important section key is ``ports`` which contains list of port scans.
For every port scan the keys presented below are available:

* id - scan identifier
* url - :doc:`url of port scan<port_scans>`
* port - port object:
    * port_number - port number
    * protocol - port protocol
    * node - node in format ``ip[id]``
* timestamp - timestamp of scan
* timestamp_human - date of scan
* scan - scanner name

Details
-------

Obtains port scan details for given id.

URL
~~~

.. code::

    /api/v1/ports/<id>

Request
~~~~~~~

.. code::

    curl "http://localhost:1235/api/v1/ports/77"


Response
~~~~~~~~

.. code-block:: json

    {
      "id": 77,
      "url": "http://localhost:1235/api/v1/port/77",
      "timestamp": 1508317322.1307728,
      "human_timestamp": "2017-10-18T09:02:02.130773+00:00",
      "port_number": 623,
      "protocol": "UDP",
      "node": {
        "id": 25,
        "ip": "10.12.2.202"
      },
      "scan": {
        "id": 93,
        "url": "http://localhost:1235/api/v1/scans/93",
        "start": 1508317320.2536325,
        "start_human": "2017-10-18T09:02:00.253633+00:00",
        "end": 1508317322.1295497,
        "end_human": "2017-10-18T09:02:02.129550+00:00",
        "protocol": null,
        "scanner": "tools_basic"
      },
      "scans": [
        {
          "id": 986,
          "url": "http://localhost:1235/api/v1/scan/986",
          "start": 1508513043.0126145,
          "start_human": "2017-10-20T15:24:03.012614+00:00",
          "end": 1508513045.4429624,
          "end_human": "2017-10-20T15:24:05.442962+00:00",
          "protocol": null,
          "scanner": "tools_basic",
          "scanner_url": "http://localhost:1235/api/v1/scanner/tools_basic"
        },
        {
          "id": 982,
          "url": "http://localhost:1235/api/v1/scan/982",
          "start": 1508512860,
          "start_human": "2017-10-20T15:21:00+00:00",
          "end": 1508512941.3509648,
          "end_human": "2017-10-20T15:22:21.350965+00:00",
          "protocol": "UDP",
          "scanner": "udp",
          "scanner_url": "http://localhost:1235/api/v1/scanner/udp"
        }
      ],
      "meta": {
        "timestamp": 1508832075.0708394,
        "human_timestamp": "2017-10-24T08:01:15.070839+00:00"
      }
    }

In the response the keys listed below are related to port scan details

* id - port scan id
* url - port scan url
* timestamp - timestamp of scan
* timestamp_human - date of scan
* port_number - port number
* protocol - port protocol
* node
    * id - id of node
    * ip - ip address of node
* scan - scan object
* scans - list of last scans (30) performed on port
