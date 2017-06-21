import ipaddress
from unittest import TestCase
from unittest.mock import patch, MagicMock

from tornado.testing import gen_test, AsyncTestCase

from fixtures.exploits import Exploit
from structs import RiskLevel, Port, Node, TransportProtocol, Scan
from tools.skipfish.tool import SkipfishTool


class SkipfishToolTest(AsyncTestCase):
    def setUp(self):
        super(SkipfishToolTest, self).setUp()
        self.exploit = Exploit(exploit_id=1)
        self.exploit.name = 'skipfish'
        self.exploit.risk_level = RiskLevel.NONE

        self.config = {}

        self.exploits = [self.exploit]
        self.port = Port(node=Node(node_id=1, ip=ipaddress.ip_address('127.0.0.1')), number=3,
                         transport_protocol=TransportProtocol.TCP)
        self.port.scan = Scan(start=13, end=45)

        self.aucote = MagicMock()
        self.skipfish_tool = SkipfishTool(aucote=self.aucote, exploits=self.exploits, port=self.port,
                                          config=self.config)

    @patch('tools.skipfish.tool.SkipfishScanTask')
    @gen_test
    async def test_call(self, skipfish_scan_mock):
        await self.skipfish_tool()

        skipfish_scan_mock.assert_called_once_with(aucote=self.aucote, port=self.port,
                                                   exploits=[self.aucote.exploits.find.return_value])

    @patch('aucote_cfg.cfg.get', MagicMock(return_value=False))
    @gen_test
    async def test_disable(self):
        config = MagicMock()
        await SkipfishTool(exploits=MagicMock(), port=MagicMock(is_ipv6=False), aucote=self.aucote, config=config)()

        self.assertEqual(config.get.call_count, 0)

    @patch('aucote_cfg.cfg.get', MagicMock(return_value=True))
    @patch('tools.skipfish.tool.SkipfishScanTask')
    @gen_test
    async def test_disable_ipv6(self, mock_scantask):
        config = MagicMock()
        await SkipfishTool(exploits=MagicMock(), port=MagicMock(is_ipv6=True), aucote=self.aucote, config=config)()

        self.assertFalse(mock_scantask.called)
