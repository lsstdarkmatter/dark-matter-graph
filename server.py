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
    from http.server import HTTPServer, SimpleHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def address_string(self):
        return self.client_address[0]

    def finish(self):
        if not self.wfile.closed:
            try:
                self.wfile.flush()
            except socket.error:
                self.wfile._wbuf = []
                self.wfile._wbuf_len = 0
        self.wfile.close()
        self.rfile.close()


def find_open_port():
    for port in range(8887, 8080, -1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            try:
                s.bind(('', port))
            except socket.error:
                pass
            else:
                return port


def serve_http(port):
    with open(os.devnull, 'w') as devnull:
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            httpd = HTTPServer(('', port), MyHTTPRequestHandler)
            httpd.serve_forever()
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            httpd.server_close()


def main(port=None, browser=True, **kwargs):
    port = port or find_open_port()
    url = 'http://127.0.0.1:{}'.format(port)

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
