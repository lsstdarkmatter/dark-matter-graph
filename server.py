#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import subprocess
import socket
import webbrowser
import argparse
from contextlib import closing

def find_open_ports():
    for port in range(8887, 8080, -1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            try:
                s.bind(("", port))
            except socket.error:
                pass
            else:
                return port


def main(port=None, browser=True, **kwargs):
    port = port or find_open_ports()
    url = "http://127.0.0.1:{}".format(port)
    is_py2 = (sys.version_info[0] == 2)
    cmd = ['python', '-m', 'SimpleHTTPServer' if is_py2 else 'http.server', '{}'.format(port)]

    try:
        with open(os.devnull, 'w') as devnull:
            p = subprocess.Popen(cmd, stdout=devnull, stderr=devnull)

            print()
            print("Server running. Open browser and visit => {}".format(url))
            print("To exit, press ctrl + c")
            print()

            if browser:
                webbrowser.open(url, new=2, autoraise=True)

            p.wait()

    except (KeyboardInterrupt, SystemExit):
        print(" Bye!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', metavar='PORT', dest='port', type=int)
    parser.add_argument('--no-browser', dest='browser', action='store_false')
    main(**vars(parser.parse_args()))
