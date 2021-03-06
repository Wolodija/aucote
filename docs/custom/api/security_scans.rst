Security scans
==============

List
----

Obtains list of security scans from Aucote's storage. Security scan is a connection between exploit, port and scan.
Single security scan provides information about timestamp of scan of specific port by given exploit.

URL
~~~

.. code::

    /api/v1/security_scans?limit=<limit>&page=<page>


Parameters limit and offset are optional. Limit defines how many rows should be returned 
and page defines page of results. First page has number 0.

For parameters ``limit=10``, ``offset=3`` the rows from 30 to 39 will be displayed.

Request
~~~~~~~

.. code::

    curl "http://localhost:1235/api/v1/security_scans?limit=2&page=13"


Response
~~~~~~~~

.. code:: json

    {
      "security_scans": [
        {
          "id": 12482,
          "url": "http://localhost:1235/api/v1/security_scans/12482",
          "port": {
            "port_number": 5985,
            "protocol": "TCP",
            "node": {
              "id": 86,
              "ip": "10.12.2.175"
            }
          },
          "scan": {
            "id": 942,
            "url": "http://localhost:1235/api/v1/scans/942",
            "start": 1508504400.6845937,
            "start_human": "2017-10-20T13:00:00.684594+00:00",
            "end": 1508504411.276814,
            "end_human": "2017-10-20T13:00:11.276814+00:00",
            "protocol": null,
            "scanner": "tools_advanced",
            "scanner_url": "http://localhost:1235/api/v1/scanners/tools_advanced"
          },
          "scan_end": 1508505422,
          "scan_end_human": "2017-10-20T13:17:02+00:00",
          "scan_start": 1508504395.823977,
          "scan_start_human": "2017-10-20T12:59:55.823977+00:00",
          "exploit": {
            "id": 71,
            "app": "nmap",
            "name": "http-vuln-cve2010-2861"
          }
        },
        {
          "id": 12483,
          "url": "http://localhost:1235/api/v1/security_scans/12483",
          "port": {
            "port_number": 5985,
            "protocol": "TCP",
            "node": {
              "id": 86,
              "ip": "10.12.2.175"
            }
          },
          "scan": {
            "id": 942,
            "url": "http://localhost:1235/api/v1/scans/942",
            "start": 1508504400.6845937,
            "start_human": "2017-10-20T13:00:00.684594+00:00",
            "end": 1508504411.276814,
            "end_human": "2017-10-20T13:00:11.276814+00:00",
            "protocol": null,
            "scanner": "tools_advanced",
            "scanner_url": "http://localhost:1235/api/v1/scanners/tools_advanced"
          },
          "scan_end": 1508505422,
          "scan_end_human": "2017-10-20T13:17:02+00:00",
          "scan_start": 1508504395.823977,
          "scan_start_human": "2017-10-20T12:59:55.823977+00:00",
          "exploit": {
            "id": 72,
            "app": "nmap",
            "name": "http-vuln-cve2011-3192"
          }
        }
      ],
      "navigation": {
        "limit": 2,
        "page": 13,
        "next_page": "http://localhost:1235/api/v1/security_scans?limit=2&page=14",
        "previous_page": "http://localhost:1235/api/v1/security_scans?limit=2&page=12"
      },
      "meta": {
        "timestamp": 1508833364.4385674,
        "human_timestamp": "2017-10-24T08:22:44.438567+00:00"
      }
    }


The most important section key is ``security_scans`` which contains list of security scans.
For every security scan the keys presented below are available:

* id - security scan identifier
* url - [url of security scan](security_scans.md)
* port - port object:
    * port_number - port number
    * protocol - port protocol
    * node
        * id - id of node
        * ip - ip address of node
* scan - [scan object](scans.md)
* scan_end - security  scan end timestamp
* scan_end_human - date of security scan end
* scan_start - security scan start timestamp
* scan_start_human - date of security scan start
* exploit - exploit object
    * id - id of exploit
    * app - name of exploit app
    * name - name of script

Details
-------

Obtains security scan details for given id.

URL
~~~

.. code::

    /api/v1/security_scans/<id>

Request
~~~~~~~

.. code::

    curl "http://localhost:1235/api/v1/security_scans/12483"


Response
~~~~~~~~

.. code:: json

    {
      "id": 12483,
      "url": "http://localhost:1235/api/v1/security_scans/12483",
      "port": {
        "port_number": 5985,
        "protocol": "TCP",
        "node": {
          "id": 86,
          "ip": "10.12.2.175"
        }
      },
      "scan": {
        "id": 942,
        "url": "http://localhost:1235/api/v1/scans/942",
        "start": 1508504400.6845937,
        "start_human": "2017-10-20T13:00:00.684594+00:00",
        "end": 1508504411.276814,
        "end_human": "2017-10-20T13:00:11.276814+00:00",
        "protocol": null,
        "scanner": "tools_advanced",
        "scanner_url": "http://localhost:1235/api/v1/scanners/tools_advanced"
      },
      "scan_end": 1508505422,
      "scan_end_human": "2017-10-20T13:17:02+00:00",
      "scan_start": 1508504395.823977,
      "scan_start_human": "2017-10-20T12:59:55.823977+00:00",
      "exploit": {
        "id": 72,
        "app": "nmap",
        "name": "http-vuln-cve2011-3192"
      },
      "scan_url": "http://localhost:1235/api/v1/scans/942",
      "scans": [
        {
          "id": 942,
          "url": "http://localhost:1235/api/v1/scans/942",
          "start": 1508504400.6845937,
          "start_human": "2017-10-20T13:00:00.684594+00:00",
          "end": 1508504411.276814,
          "end_human": "2017-10-20T13:00:11.276814+00:00",
          "protocol": null,
          "scanner": "tools_advanced",
          "scanner_url": "http://localhost:1235/api/v1/scanners/tools_advanced"
        },
        {
          "id": 931,
          "url": "http://localhost:1235/api/v1/scans/931",
          "start": 1508503680.2786627,
          "start_human": "2017-10-20T12:48:00.278663+00:00",
          "end": 1508503687.3294709,
          "end_human": "2017-10-20T12:48:07.329471+00:00",
          "protocol": null,
          "scanner": "tools_basic",
          "scanner_url": "http://localhost:1235/api/v1/scanners/tools_basic"
        }
      ],
      "meta": {
        "timestamp": 1508833683.8892133,
        "human_timestamp": "2017-10-24T08:28:03.889213+00:00"
      }
    }

In the response the keys listed below are related to port scan details

* id - port scan id
* url - port scan url
* port - port object
    * port_number - port number
    * protocol - port protocol
    * node
        * id - id of node
        * ip - ip address of node
* timestamp - timestamp of scan
* timestamp_human - date of scan
* scan - :doc:`scan object<scans>`
* scan_url - url of :doc:`scan<scans>`
* scan_end - security scan end timestamp
* scan_end_human - date of security  scan end
* scan_start - security scan start timestamp
* scan_start_human - date of security scan start
* exploit - exploit object
    * id - id of exploit
    * app - name of exploit app
    * name - name of script
* scans - list of last scans (30) performed on port for given exploit. Scans are formatted like :doc:`scans<scans>`
