import ipaddress
from unittest import TestCase
from unittest.mock import MagicMock, patch

from fixtures.exploits import Exploit
from structs import Port, TransportProtocol, Node
from tools.base import Tool
from utils.exceptions import ImproperConfigurationException


class ToolTest(TestCase):
    def setUp(self):
        self.executor = MagicMock()
        self.executor.storage.filename = ":memory:"
        self.exploits = MagicMock()
        self.config = MagicMock()
        self.port = MagicMock()

        self.tool = Tool(executor=self.executor, exploits=self.exploits, port=self.port, config=self.config)

    def test_init(self):
        self.assertEqual(self.tool.executor, self.executor)
        self.assertEqual(self.tool.exploits, self.exploits)
        self.assertEqual(self.tool.config, self.config)
        self.assertEqual(self.tool.port, self.port)

    def test_call(self):
        self.assertRaises(NotImplementedError, self.tool)

    @patch('tools.nmap.tool.cfg.get')
    def test_get_config_non_exist_key(self, mock_cfg):
        mock_cfg.side_effect = KeyError

        self.assertRaises(ImproperConfigurationException, Tool.get_config, 'non.exist.key')

    @patch('tools.nmap.tool.cfg.get')
    def test_get_config_exist_key(self, mock_cfg):
        expected =  {"key": []}
        mock_cfg.return_value.cfg = expected
        result = Tool.get_config('key')

        self.assertEqual(result, expected)