import ipaddress
import subprocess
from unittest import TestCase
from unittest.mock import patch, MagicMock

from structs import Node
from tools.masscan import MasscanPorts

class MasscanPortsTest(TestCase):
    '''
    Test masscan port scanning.
    '''

    NODE_IP = '127.0.0.1'
    NODE_NAME = 'localhost'
    MASSSCAN_OUTPUT_XML = """<?xml version="1.0"?>
<!-- masscan v1.0 scan -->
<?xml-stylesheet href="" type="text/xsl"?>
<nmaprun scanner="masscan" start="1470387319" version="1.0-BETA"  xmloutputversion="1.03">
<scaninfo type="syn" protocol="tcp" />
<host endtime="1470387319"><address addr="127.0.0.1" addrtype="ipv4"/><ports><port protocol="tcp" portid="514"><state state="open" reason="syn-ack" reason_ttl="62"/></port></ports></host>
<host endtime="1470387319"><address addr="127.0.0.1" addrtype="ipv4"/><ports><port protocol="tcp" portid="80"><state state="open" reason="syn-ack" reason_ttl="62"/></port></ports></host>
<runstats>
<finished time="1470387330" timestr="2016-08-05 10:55:30" elapsed="13" />
<hosts up="2" down="0" total="2" />
</runstats>
</nmaprun>
"""
    NON_XML = '''This is non xml output!'''

    def setUp(self):
        self.masscanports = MasscanPorts()
        node = Node()
        node.ip = ipaddress.ip_address(self.NODE_IP)
        node.name = None
        node.id = None
        self.nodes = [node]

    @patch('subprocess.check_output', MagicMock(return_value=MASSSCAN_OUTPUT_XML))
    def test_stdout(self):
        ports = self.masscanports.scan_ports(self.nodes)
        self.assertEqual(len(ports), 2)


    @patch('subprocess.check_output', MagicMock(side_effect=subprocess.CalledProcessError(returncode=1, cmd='masscan')))
    def test_stderr(self):
        self.assertRaises(SystemExit, self.masscanports.scan_ports, self.nodes)

    @patch('subprocess.check_output', MagicMock(return_value=NON_XML))
    def test_without_xml_output(self):
        ports = self.masscanports.scan_ports(self.nodes)
        self.assertEqual(len(ports), 0)
