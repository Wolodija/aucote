"""
Base class for all of Aucote's request handlers

"""
import functools
import hashlib

from tornado.web import RequestHandler

from aucote_cfg import cfg


class Handler(RequestHandler):
    """
    Defines common properties for handler

    """
    SCANNER_URL = '/api/v1/scanners/{scanner_name}'
    SCAN_URL = '/api/v1/scans/{scan_id}'
    NODES_SCAN_URL = '/api/v1/nodes/{node_scan_id}'
    PORTS_SCAN_URL = '/api/v1/ports/{port_scan_id}'
    SECURITY_SCAN_URL = '/api/v1/security_scans/{sec_scan_id}'
    VULNERABILITY_URL = '/api/v1/vulnerabilities/{vuln_id}'

    def initialize(self, aucote, path=''):
        """
        Integrates Handlers with aucote

        Args:
            aucote (Aucote):

        Returns:
            None

        """
        self.aucote = aucote
        path = path.strip('/')
        self.path = ('/' + path) if path else ''

    @staticmethod
    def auth(handler_class):
        """
        Handler for authorization

        Args:
            handler_class:

        Returns:

        """
        MAX_PASSWORD_HEADER_LENGTH = 80
        BEARER_START = 'Bearer '

        def wrap_execute(handler_execute):
            """
            Authorize request

            Args:
                handler_execute:

            Returns:

            """
            def require_auth(handler, *args, **kwargs):
                """
                Authorize request

                Args:
                    handler:
                    *args:
                    **kwargs:

                Returns:
                    bool

                """
                auth_header = handler.request.headers.get('Authorization')

                if auth_header is not None and len(auth_header) < MAX_PASSWORD_HEADER_LENGTH \
                        and auth_header.startswith(BEARER_START):
                    password = auth_header[len(BEARER_START):]
                    password_hash = hashlib.sha512(password.encode()).hexdigest()
                    correct = cfg['service.api.password']

                    if password_hash == correct:
                        return True

                handler.set_status(401)
                handler._transforms = []
                handler.finish()
                return False

            def _execute(self, transforms, *args, **kwargs):
                if not require_auth(self, kwargs):
                    return False
                return handler_execute(self, transforms, *args, **kwargs)

            return _execute

        handler_class._execute = wrap_execute(handler_class._execute)
        return handler_class

    @staticmethod
    def limit(function):
        @functools.wraps(function)
        def return_value(self, *args, **kwargs):
            for key in ('limit', 'page'):
                value = self.get_query_arguments(key)

                if value and value[0].isdecimal():
                    kwargs[key] = int(value[0])

            return function(self, *args, **kwargs)

        return return_value

    def not_found(self, msg):
        """
        Set HTTP status to '404 NOT FOUND' and return dict with details (msg)

        """
        self.set_status(404, msg)
        return {'code': msg}

    def internal_error(self, msg):
        """
        Set HTTP status to '500 INTERNAL SERVER ERROR' and return dict with details (msg)

        """
        self.set_status(500, msg)
        return {'code': msg}
