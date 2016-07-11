from .nmap_scripts_cfg import SERVICE_TO_SCRIPTS, PORT_TO_SCRIPTS
import logging as log
from scans.tasks import NmapPortScanTask

class TaskMapper:
    '''
    Assign tasks for a provided port
    '''

    def __init__(self, executor):
        self._executor = executor

    def assign_tasks(self, port):
        #nmap_scripts
        all_scripts = set()
        all_scripts.update(SERVICE_TO_SCRIPTS.get(port.service_name, tuple()))
        all_scripts.update(PORT_TO_SCRIPTS.get(port.number, tuple()))
        self._executor.add_task(NmapPortScanTask(port, all_scripts))