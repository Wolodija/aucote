import ipaddress
from unittest import TestCase
from unittest.mock import MagicMock, patch

from fixtures.exploits import Exploit
from structs import Port, Node, TransportProtocol, Vulnerability
from tools.ssl.base import SSLBase
from tools.ssl.structs import SSLResults
from tools.ssl.tasks import SSLScriptTask


class SSLScriptTaskTest(TestCase):
    def setUp(self):
        exploit = Exploit(exploit_id=3)
        port = Port(node=Node(node_id=2, ip=ipaddress.ip_address('127.0.0.1')),
                    transport_protocol=TransportProtocol.UDP, number=16)
        aucote = MagicMock()
        self.task = SSLScriptTask(port=port, exploits=[exploit], aucote=aucote)

    def test_init(self):
        self.assertIsInstance(self.task.command, SSLBase)
        self.assertFalse(self.task.command.RAISE_ERROR)

    def test_prepare_args(self):
        result = self.task.prepare_args()
        expected = ['127.0.0.1']
        self.assertEqual(result, expected)

    @patch('tools.ssl.tasks.Vulnerability')
    def test_get_vulnerabilities(self, mock_vulnerability):
        data = MagicMock()
        result = self.task._get_vulnerabilities(data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], mock_vulnerability.return_value)
        mock_vulnerability.assert_called_once_with(exploit=self.task.exploit, port=self.task.port,
                                                   output=data.with_severity_ge().output)
