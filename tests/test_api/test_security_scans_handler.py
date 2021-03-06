import json
from tests.test_api.test_api import APITest


class SecurityScansHandlerTest(APITest):
    def setUp(self):
        super(SecurityScansHandlerTest, self).setUp()

    def test_security_scans(self):
        self.maxDiff = None
        expected = {
            'navigation': {
                'limit': 10,
                'next_page': self.get_url('/api/v1/security_scans?limit=10&page=1'),
                'page': 0,
                'previous_page': self.get_url('/api/v1/security_scans?limit=10&page=0')
            },
            'security_scans':
                [
                    {
                        'exploit':
                            {
                                'app': 'test_app',
                                'id': 14,
                                'name': 'test_name'
                            },
                        'id': 3,
                        'port':
                            {
                                'node': '10.156.67.18[13]',
                                'port_number': 34,
                                'protocol': 'UDP'
                            },
                        'scan_start': 114.0,
                        'scan_start_human': '1970-01-01T00:01:54+00:00',
                        'scan':
                            {
                                'end': 447,
                                'end_human': '1970-01-01T00:07:27+00:00',
                                'id': 2,
                                'protocol': 'UDP',
                                'scanner': 'udp',
                                'start': 230,
                                'start_human': '1970-01-01T00:03:50+00:00',
                                'url': self.get_url('/api/v1/scans/2')
                            },
                        'scan_end': 981.0,
                        'scan_end_human': '1970-01-01T00:16:21+00:00',
                        'url': self.get_url('/api/v1/security_scans/3')
                    },
                    {
                        'exploit':
                            {
                                'app': 'test_app',
                                'id': 14,
                                'name': 'test_name'
                            },
                        'id': 1,
                        'port':
                            {
                                'node': '10.156.67.18[13]',
                                'port_number': 34,
                                'protocol': 'UDP'
                            },
                        'scan_start': 178.0,
                        'scan_start_human': '1970-01-01T00:02:58+00:00',
                        'scan':
                            {
                                'end': 446,
                                'end_human': '1970-01-01T00:07:26+00:00',
                                'id': 1,
                                'protocol': 'TCP',
                                'scanner': 'tcp',
                                'start': 123,
                                'start_human': '1970-01-01T00:02:03+00:00',
                                'url': self.get_url('/api/v1/scans/1')
                            },
                        'scan_end': 851.0,
                        'scan_end_human': '1970-01-01T00:14:11+00:00',
                        'url': self.get_url('/api/v1/security_scans/1')
                    },
                    {
                        'exploit':
                            {
                                'app': 'test_app_2',
                                'id': 2,
                                'name': 'test_name_2'
                            },
                        'id': 2,
                        'port':
                            {
                                'node': '10.156.67.18[13]',
                                'port_number': 34,
                                'protocol': 'UDP'
                            },
                        'scan_start': 109.0,
                        'scan_start_human': '1970-01-01T00:01:49+00:00',
                        'scan':
                            {
                                'end': 446,
                                'end_human': '1970-01-01T00:07:26+00:00',
                                'id': 1,
                                'protocol': 'TCP',
                                'scanner': 'tcp',
                                'start': 123,
                                'start_human': '1970-01-01T00:02:03+00:00',
                                'url': self.get_url('/api/v1/scans/1')
                            },
                        'scan_end': 775.0,
                        'scan_end_human': '1970-01-01T00:12:55+00:00',
                        'url': self.get_url('/api/v1/security_scans/2')
                    }
                ]
        }

        response = self.fetch('/api/v1/security_scans', method='GET')

        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers['Content-Type'], "application/json; charset=UTF-8")
        result = json.loads(response.body.decode())
        del result['meta']
        self.assertEqual(result, expected)

    def test_node_details(self):
        expected = {
            'exploit': {
                'app': 'test_app', 'id': 14, 'name': 'test_name'
            },
            'id': 1,
            'port': {
                'node': '10.156.67.18[13]',
                'port_number': 34,
                'protocol': 'UDP'
            },
            'scan_start': 178.0,
            'scan': {
                'end_human': '1970-01-01T00:07:26+00:00',
                'start_human': '1970-01-01T00:02:03+00:00',
                'end': 446,
                'id': 1,
                'protocol': 'TCP',
                'scanner': 'tcp',
                'start': 123,
                'url': self.get_url('/api/v1/scans/1')
            },
            'scan_end': 851.0,
            'scan_end_human': '1970-01-01T00:14:11+00:00',
            'scan_start_human': '1970-01-01T00:02:58+00:00',
            'scan_url': self.get_url('/api/v1/scans/1'),
            'scans': [
                {
                    'end_human': '1970-01-01T00:07:27+00:00',
                    'start_human': '1970-01-01T00:03:50+00:00',
                    'end': 447,
                    'id': 2,
                    'protocol': 'UDP',
                    'scanner': 'udp',
                    'start': 230,
                    'url': self.get_url('/api/v1/scans/2')
                },
                {
                    'end_human': '1970-01-01T00:07:26+00:00',
                    'start_human': '1970-01-01T00:02:03+00:00',
                    'end': 446,
                    'id': 1,
                    'protocol': 'TCP',
                    'scanner': 'tcp',
                    'start': 123,
                    'url': self.get_url('/api/v1/scans/1')
                }
            ],
            'url': self.get_url('/api/v1/security_scans/1')
        }

        response = self.fetch('/api/v1/security_scans/1', method='GET')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers['Content-Type'], "application/json; charset=UTF-8")
        result = json.loads(response.body.decode())
        del result['meta']
        self.assertEqual(result, expected)
