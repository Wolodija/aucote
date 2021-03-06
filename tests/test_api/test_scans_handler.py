import json
from unittest.mock import MagicMock, patch

import ipaddress
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from api.scans_handler import ScansHandler
from scans.tcp_scanner import TCPScanner
from scans.tools_scanner import ToolsScanner
from structs import Node, Scan, TransportProtocol, Port, PortScan, NodeScan
from tests.test_api.test_api import APITest
from utils import Config


class ScansHandlerTest(APITest):
    def setUp(self):
        super(ScansHandlerTest, self).setUp()
        self.handler = ScansHandler(self.app, MagicMock(), aucote=self.aucote)

    def test_scans(self):
        expected = {
            'navigation': {
                'limit': 10,
                'next_page': self.get_url('/api/v1/scans?limit=10&page=1'),
                'page': 0,
                'previous_page': self.get_url('/api/v1/scans?limit=10&page=0')
            },
            "scans":
                [
                    {
                        'id': 2,
                        'url': self.get_url('/api/v1/scans/2'),
                        'protocol': 'UDP',
                        'start': 230,
                        'end': 447,
                        'end_human': '1970-01-01T00:07:27+00:00',
                        'start_human': '1970-01-01T00:03:50+00:00',
                        'scanner': 'udp'
                    },
                    {
                        'id': 1,
                        'url': self.get_url('/api/v1/scans/1'),
                        'protocol': 'TCP',
                        'end_human': '1970-01-01T00:07:26+00:00',
                        'start_human': '1970-01-01T00:02:03+00:00',
                        'start': 123,
                        'end': 446,
                        'scanner': 'tcp'
                    }
                ]
        }
        response = self.fetch('/api/v1/scans', method='GET')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers['Content-Type'], "application/json; charset=UTF-8")
        result = json.loads(response.body.decode())
        del result['meta']
        self.assertEqual(result, expected)

    def test_scan(self):
        expected = {
            "scan": 1,
            "url": self.get_url('/api/v1/scans/1'),
            "end": 446,
            'end_human': '1970-01-01T00:07:26+00:00',
            "start": 123,
            'start_human': '1970-01-01T00:02:03+00:00',
            "nodes_scans": [
                {
                    'id': 1,
                    'ip': '10.156.67.18',
                    "url": self.get_url('/api/v1/nodes/1'),
                    "node_id": 13,
                    "scan": 'tcp'
                }
            ],
            "ports_scans":
                [
                    {
                        'id': 2,
                        'port': {
                            'node': '10.156.67.34[75]',
                            'port_number': 78,
                            'protocol': 'TCP'
                        },
                        'scan': 'tcp',
                        'timestamp': 2345,
                        'timestamp_human': '1970-01-01T00:39:05+00:00',
                        'url': self.get_url('/api/v1/ports/2')
                    },
                    {
                        'id': 1,
                        'port': {
                            'node': '10.156.67.18[13]',
                            'port_number': 34,
                            'protocol': 'UDP',
                        },
                        'scan': 'tcp',
                        'timestamp': 1234,
                        'timestamp_human': '1970-01-01T00:20:34+00:00',
                        'url': self.get_url('/api/v1/ports/1')
                    }
                ]
        }
        response = self.fetch('/api/v1/scans/1', method='GET')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers['Content-Type'], "application/json; charset=UTF-8")
        result = json.loads(response.body.decode())
        del result['meta']
        self.assertEqual(result, expected)
