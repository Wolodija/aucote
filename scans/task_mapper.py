"""
Maps scans to ports and services. This module is also for filtering based on configuration

"""
import logging as log

from aucote_cfg import cfg
from scans.executor_config import EXECUTOR_CONFIG
from structs import SpecialPort, TaskManagerType


class TaskMapper(object):
    """
    Assign tasks for a provided port

    """

    def __init__(self, context):
        """
        Args:
            executor (Executor): tasks executor
            scan (Scan): Scan under which the mapper is working

        """
        self.context = context
        self.scanner = context.scanner

    @property
    def _aucote(self):
        return self.context.aucote

    @property
    def scan(self) -> 'Scan':
        """
        Scanner's Scan
        """
        return self.context.scanner.scan

    async def assign_tasks(self, port, scripts=None):
        """

        Args:
            port (Port):
            scripts (list|None): list of exploits or None, which stands for all exploits

        Returns:

        """
        scripts = scripts or self._aucote.exploits.find_all_matching(port)

        for app, exploits in scripts.items():
            if not cfg['tools.{0}.enable'.format(app)]:
                continue

            log.info("Found %i exploits (%s) for %s", len(exploits), app, port)

            if not isinstance(port, SpecialPort):
                exploits = self._filter_exploits(exploits)

            log.info("Using %i exploits against %s", len(exploits), port)
            self.store_security_scan(port=port, exploits=exploits)
            task = EXECUTOR_CONFIG['apps'][app]['class'](context=self.context, exploits=exploits, port=port.copy(),
                                                         config=EXECUTOR_CONFIG['apps'][app])

            self.context.add_task(task, manager=TaskManagerType.QUICK)

    async def assign_tasks_for_node(self, node: 'Node') -> None:
        """
        Assign tasks for provided node
        """
        apps = EXECUTOR_CONFIG['node_scan']
        scripts = self._aucote.exploits.find_by_apps(apps)

        for app, exploits in scripts.items():
            if not cfg['tools.{0}.enable'.format(app)]:
                continue
            exploits = self._filter_exploits(exploits)

            log.info("Using %i exploits against %s", len(exploits), node)

            task = EXECUTOR_CONFIG['apps'][app]['class'](context=self.context, exploits=exploits, node=node,
                                                         config=EXECUTOR_CONFIG['apps'][app])

            self.context.add_task(task, manager=TaskManagerType.QUICK)

    def _filter_exploits(self, exploits):
        return list(filter(self._is_exploit_allowed, exploits))

    def _is_exploit_allowed(self, exploit):
        if not self.scanner.is_exploit_allowed(exploit):
            log.debug("Exploit %s is not allowed by scanner (%s) configuration", str(exploit), self.scanner.NAME)
            return False

        return True

    @property
    def exploits(self):
        """
        Executor's exploits

        """
        return self._aucote.exploits

    def store_security_scan(self, port, exploits):
        """
        Saves scan details into storage

        Args:
            port (Port):
            exploits (Exploits):

        Returns:
            None
        """
        self.storage.save_security_scans(exploits=exploits, port=port, scan=self.scan)

    @property
    def storage(self):
        """
        Aucote's storage

        Returns:
            Storage

        """
        return self._aucote.storage
