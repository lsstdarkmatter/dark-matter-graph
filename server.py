#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import socket
from contextlib import closing
try:
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer
except ImportError:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer


_ADDRESS = '127.0.0.1'


def find_open_ports():
    for port in range(8887, 8080, -1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            try:
                s.bind((_ADDRESS, port))
            except socket.error:
                pass
            else:
                return port


if __name__ == "__main__":
    port = find_open_ports()
    print()
    print("Server running. Open browser and visit => http://{}:{}".format(_ADDRESS, port))
    print("To stop, press Ctrl+C{}.".format(' (may need to press more than once)' if sys.version_info[0]==2 else ''))
    print()

    with open(os.devnull, "w") as devnull:
        sys.stderr = devnull
        try:
            httpd = TCPServer((_ADDRESS, port), SimpleHTTPRequestHandler)
            try:
                httpd.serve_forever()
            except BaseException:
                print(" Bye!")
            finally:
                httpd.shutdown()
                httpd.server_close()
        finally:
            sys.stderr = sys.__stderr__
