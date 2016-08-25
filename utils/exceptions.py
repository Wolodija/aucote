"""
Custom exceptions used by aucote project
"""

class NonXMLOutputException(BaseException):
    """
    Raise if output should be xml but it isn't
    """


class HydraPortMismatchException(BaseException):
    """
    Raise if port number from output is different than expected
    """


class NmapUnsupported(NameError):
    """
    abstract class for exception raised if protocols, ports or services are unsupported by nmap
    """

class ServiceUnsupporedByNmapException(NmapUnsupported):
    """
    Raise if service name does not exist in nmap services file
    """


class PortUnsupportedException(NmapUnsupported):
    """
    Raise if service name does not exist in nmap services file
    """


class ProtocolUnsupporedByNmapException(NmapUnsupported):
    """
    Raise if service name does not exist in nmap services file
    """
