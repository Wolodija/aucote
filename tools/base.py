"""
Defines abstract Tool class
"""


class Tool(object):
    """
    Tool is a object, which can execute one of more scripts, e.g. Nmap, Hydra
    """
    def __init__(self, executor, exploits, port, config):
        """
        Init values needed to run and proceed command
        """
        self.executor = executor
        self.exploits = exploits
        self.config = config
        self.port = port

    def __call__(self, *args, **kwargs):
        """
        Called by task managers
        """
        raise NotImplementedError