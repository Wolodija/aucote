from structs import Vulnerability
from tools.common.command import CommandXML


class NmapBase(CommandXML):
    '''
    Base for all classes using nmap application.
    '''
    COMMON_ARGS = ('-n', '--privileged', '-oX', '-', '-T4')
    NAME = 'nmap'


class NmapScript(object):
    def __init__(self, port, exploit, name=None, args=None):
        self.exploit = exploit
        self.port = port
        self.name = name
        self.args = args

    def handle(self, script):
        vuln = self.get_vulnerability(script)
        if vuln == None: return None
        vuln.exploit = self.exploit
        vuln.port = self.port
        vuln.output = script.get('output').strip()
        return vuln

    def get_vulnerability(self, script):
        raise NotImplementedError


class VulnNmapScript(NmapScript):
    def get_vulnerability(self, script):
        table = script.find('table')
        if table is None: return None #no data, probably no response from server, so no problem detected
        state = table.find("./elem[@key='state']").text
        if state not in ('VULNERABLE', 'LIKELY VULNERABLE'): return None #TODO: add likelihood to vulnerability
        return Vulnerability()


class InfoNmapScript(NmapScript):
    def get_vulnerability(self, script):
        return Vulnerability()


