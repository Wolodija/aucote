"""
Provide class for tasks

"""
import logging as log
import time
from threading import Lock

from database.serializer import Serializer


class Task(object):
    """
    Base class for tasks, e.g. scan, nmap, hydra

    """
    def __init__(self, aucote):
        """
        Assign executor

        """
        self._lock = Lock()
        self.aucote = aucote
        self.creation_time = time.time()
        self.start_time = None
        self._name = None

    @property
    def kudu_queue(self):
        """
        Return executors kudu_queue

        """
        return self.aucote.kudu_queue

    # @property
    # def exploits(self):
    #     """
    #     Return executors exploits
    #
    #     """
    #     return self.aucote.exploits

    def __call__(self, *args, **kwargs):
        """
        Call executed by executor

        """
        raise NotImplementedError

    def send_msg(self, msg):
        """
        Send msg to kudu_queue

        """
        return self.kudu_queue.send_msg(msg)

    def store_scan_end(self, exploits, port):
        """
        Stores scan end in local storage

        Args:
            exploits (Exploits):
            port (Port):

        Returns:
            None
        """
        self.aucote.storage.save_scans(exploits=exploits, port=port)

    def store_vulnerability(self, vuln):
        """
        Saves vulnerability into database (kudu)

        Args:
            vuln (Vulnerability):

        Returns:
            None

        """
        log.debug('Found vulnerability: port=%s exploit=%s output=%s', vuln.port, vuln.exploit.id, vuln.output)
        msg = Serializer.serialize_port_vuln(vuln.port, vuln)
        self.kudu_queue.send_msg(msg)

    def store_vulnerabilities(self, vulnerabilities):
        """
        Saves vulnerabilities into storage

        Args:
            vulnerabilities (list):

        Returns:
            None

        """
        log.info("Saving %i vulnerabilities", len(vulnerabilities))

        if vulnerabilities:
            for vulnerability in vulnerabilities:
                self.store_vulnerability(vulnerability)

        return None

    def reload_config(self):
        """
        Should be executed by executor when, configuration is reloaded

        Returns:
            None
        """
        pass

    @property
    def storage(self):
        """
        Storage for aucote application

        Returns:
            None
        """
        return self.aucote.storage

    @property
    def name(self):
        return self._name or type(self).__name__
