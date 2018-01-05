#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import socket
import webbrowser
import argparse
from contextlib import closing
from multiprocessing import Process

try:
    from http.server import SimpleHTTPRequestHandler, HTTPServer
except ImportError:
    from SimpleHTTPServer import SimpleHTTPRequestHandler, HTTPServer


_ADDRESS = '127.0.0.1'


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def address_string(self):
        return self.client_address[0]


def find_open_ports():
    for port in range(8887, 8080, -1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            try:
                s.bind((_ADDRESS, port))
            except socket.error:
                pass
            else:
                return port


def serve_http(port):
    with open(os.devnull, "w") as devnull:
        sys.stderr = devnull
        try:
            httpd = HTTPServer((_ADDRESS, port), MyHTTPRequestHandler)
            httpd.serve_forever()
        finally:
            sys.stderr = sys.__stderr__
            httpd.server_close()


def main(port=None, browser=True, **kwargs):
    port = port or find_open_ports()
    url = 'http://{}:{}'.format(_ADDRESS, port)

    p = Process(target=serve_http, args=(port,))
    p.start()

    print()
    print('Server running. Open browser and visit => {}'.format(url))
    print('To exit, press ctrl + c')
    print()

    if browser:
        webbrowser.open(url, new=2, autoraise=True)

    try:
        p.join()

    except (KeyboardInterrupt, SystemExit):
        p.terminate()
        print(' Bye!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', metavar='PORT', dest='port', type=int)
    parser.add_argument('--no-browser', dest='browser', action='store_false')
    main(**vars(parser.parse_args()))
