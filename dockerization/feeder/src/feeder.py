from http.server import BaseHTTPRequestHandler, HTTPServer

import yaml
import json
import logging as log


class Feeder(BaseHTTPRequestHandler):

    def get_hosts_list(self):
        with open(r'files/hosts_example.yml') as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            fruits_list = yaml.load(file)

        return fruits_list

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(self.get_hosts_list()).encode('utf8'))
        return


def run(port: int = 1234):
    log.info('starting server...')

    # Server settings
    server_address = ('feeder', port)
    httpd = HTTPServer(server_address, Feeder)
    log.info('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
