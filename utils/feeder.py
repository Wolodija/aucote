"""
feeder is a topology discovery tool. This file provide integration with it

"""
import logging as log
import time

import ujson

import ipaddress

from structs import Node, Scan, TopisOSDiscoveryType, Service, CPEType
from utils.http_client import retry_if_fail, HTTPClient
from tornado.httpclient import HTTPError

from utils.time import parse_time_to_timestamp


class Feeder(object):
    """
    feeder provides topology information which are base for all scans

    """
    min_retry_time = 5
    max_retry_time = 30
    max_retry_count = 20

    def __init__(self, hostname, port, api):
        self.api = 'http://{0}:{1}{2}'.format(hostname, port, api)

    async def get_snmp_nodes(self) -> set:
        return await self._get_nodes('nodes?ip=0&snmp=1')

    async def get_all_nodes(self) -> set:
        return await self._get_nodes('nodes?ip=1&snmp=1')

    @retry_if_fail(min_retry_time, max_retry_time, max_retry_count, HTTPError)
    async def _get_nodes(self, url: str) -> set:
        """
        Get nodes from feeder

        Returns:
            set of unique nodes (Node object)

        """
        url = '{0}/{1}'.format(self.api, url)
        resource = await HTTPClient.instance().get(url)

        hosts_cfg = ujson.loads(resource.body)

        timestamp = int(time.time())
        ip_node = {}

        idh = 0
        for host in hosts_cfg['hosts']:
                node = Node(ip=ipaddress.ip_address(host), node_id=idh)
                node.name = host
                node.scan = Scan(start=timestamp)

                ip_node[node.ip] = node
                log.info(ip_node)
        nodes = set(ip_node.values())
        log.debug(nodes)
        log.debug('Got %i nodes from feeder', len(nodes))
        return nodes
