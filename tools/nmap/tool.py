"""
Contains main class responsible for managing NMAP

"""
import logging as log
from collections import defaultdict

import itertools

from aucote_cfg import cfg
from structs import RiskLevel, TransportProtocol
from tools.base import Tool
from tools.nmap.base import NmapScript
from tools.nmap.parsers import NmapVulnParser, NmapInfoParser
from tools.nmap.tasks.port_scan import NmapPortScanTask
from utils.exceptions import ImproperConfigurationException


class NmapTool(Tool):
    """
    It's responsible for managing and executing nmap tasks

    """

    def call(self, *args, **kwargs):
        """
        Prepares nmap args, executes and manages nmap scripts.

        If there is a list of different arguments and this same script name, they shouldn't be executed together

        Args:
            *args:
            **kwargs:

        Returns:
            None

        """
        tasks = self._get_tasks()

        by_name = defaultdict(set)
        for task in tasks:
            by_name[task.name].add(task)
        packs = itertools.zip_longest(*by_name.values())

        for pack in packs:
            self.aucote.add_task(NmapPortScanTask(aucote=self.aucote, port=self.port,
                                                  script_classes=[val for val in pack if val is not None],
                                                  rate=self.rate))

    def _get_tasks(self):
        """
        Prepare nmaps scripts  for executing

        Returns:
            list - list of tasks
        """
        tasks = []

        disabled_scripts = self.config.get('disable_scripts', set()).copy()
        disabled_scripts.update(set(cfg['tools.nmap.disable_scripts'] or []))

        for exploit in self.exploits:
            name = exploit.name

            if name in disabled_scripts:
                continue

            service_args = self.config.get('services', {}).get(self.port.service_name, {}).get('args', None)

            if callable(service_args):
                service_args = service_args()
            else:
                service_args = ""

            args = self.config.get('scripts', {}).get(name, {}).get('args', None)
            singular = self.config.get('scripts', {}).get(name, {}).get('singular', False)

            if callable(args):
                try:
                    args = args()
                except ImproperConfigurationException:
                    log.warning("Please set up %s in configuration", name)
                    continue

            if not isinstance(args, (list, set)):
                args = [args]

            for arg in args:
                arg = "{0},{1}".format(arg or "", service_args).strip(",")

                parser = self.config.get('scripts', {}).get(exploit.name, {}).get('parser')

                if not parser and exploit.risk_level == RiskLevel.NONE:
                    parser = NmapInfoParser
                elif not parser:
                    parser = NmapVulnParser

                task = NmapScript(exploit=exploit, port=self.port, parser=parser(), name=name, args=arg)

                if singular:
                    self.aucote.add_task(NmapPortScanTask(aucote=self.aucote, port=self.port,
                                                          script_classes=[task], rate=self.rate))
                    continue
                tasks.append(task)

        return tasks

    @classmethod
    def custom_args_dns_zone_transfer(cls):
        """
        Parses configuration and convert it to the script argument

        Returns:
            list

        """
        domains = cfg['tools.nmap.domains']
        return ['dns-zone-transfer.domain={0}'.format(domain) for domain in domains]

    @classmethod
    def custom_args_dns_srv_enum(cls):
        """
        Parses configuration and convert it to the script argument

        Returns:
            list

        """
        domains = cfg['tools.nmap.domains']
        return ['dns-srv-enum.domain={0}'.format(domain) for domain in domains]

    @classmethod
    def custom_args_dns_check_zone(cls):
        """
        Parses configuration and convert it to the script argument

        Returns:
            list

        """
        domains = cfg['tools.nmap.domains']
        return ['dns-check-zone.domain={0}'.format(domain) for domain in domains]

    @classmethod
    def custom_args_http_domino_enum_passwords(cls):
        """
        Parses configuration and convert it to the script argument

        Returns:
            str

        """
        username = cfg['tools.nmap.domino-http.username']
        password = cfg['tools.nmap.domino-http.password']

        return "domino-enum-passwords.username='{0}',domino-enum-passwords.password={1}".format(username, password)

    @classmethod
    def custom_args_http_useragent(cls):
        """
        Parses configuration and convert it to the script argument

        Returns:
            str

        """
        config = cfg['service.scans.useragent']
        if config:
            return "http.useragent='{0}'".format(config)

    @property
    def rate(self):
        """
        Rate for Nmap scripts

        Returns:
            int

        """
        try:
            return cfg['tools.nmap.rate']
        except KeyError:
            return cfg['tools.common.rate']

    @staticmethod
    def parse_nmap_ports(sections):
        """
        Parses nmap ports argument and returns dictionary of sets

        Args:
            port_string (str):

        Returns:
            dict

        """

        return_value = {
            "T": set(),
            "U": set(),
            "S": set()
        }

        if isinstance(sections, str):
            sections = sections.split(",")

        if isinstance(sections, list):
            sections = [element for section in sections for element in section.split(",")]

        protocol = "T"

        for section in sections:
            if not section:
                continue

            if ":" in section:
                protocol = section[0]
                section = section[2:]

            if "-" in section:
                range_args = [int(el) for el in section.split("-")]
                return_value[protocol] |= set(range(range_args[0], range_args[1]+1))
                continue

            return_value[protocol] |= {int(section)}

        return {
            TransportProtocol.TCP: return_value["T"],
            TransportProtocol.UDP: return_value["U"],
            TransportProtocol.SCTP: return_value["S"]
        }
