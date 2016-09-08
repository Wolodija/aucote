import subprocess
import logging as log

import time

from aucote_cfg import cfg
from structs import Vulnerability
from tools.skipfish.base import SkipfishBase


class SkipfishScanTask(SkipfishBase):
    """
    This is task for Skipfish tool. Call skipfish and parse output
    """

    def __init__(self, port, *args, **kwargs):
        """
        Initialize variables
        """

        super().__init__(*args, **kwargs)
        self._port = port

    def __call__(self):
        """
        Call command, parse output and send to kudu_queue
        """

        args = ['-m', str(cfg.get('tools.skipfish.threads')), '-k', cfg.get('tools.skipfish.limit')]
        args.extend(['-o', '{0}/skipfish_{1}'.format(cfg.get('tools.skipfish.tmp_directory'), time.time()),
                     "{0}://{1}:{2}/".format(self._port.service_name, self._port.node.ip, self._port.number)])

        try:
            results = self.call(args)
        except subprocess.CalledProcessError as exception:
            log.warning("Exiting process", exc_info=exception)
            return None

        if not results:
            return results

        self.store_vulnerability(Vulnerability(exploit=self.exploits.find('skipfish', 'skipfish'), port=self._port,
                                               output=results))
        return results