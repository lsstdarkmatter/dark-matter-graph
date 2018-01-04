#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import subprocess
import socket
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


if __name__ == "__main__":
    port = find_open_ports()
    is_py2 = (sys.version_info[0] == 2)
    cmd = ['python', '-m', 'SimpleHTTPServer' if is_py2 else 'http.server', str(port)]

    print()
    print("Server running. Open browser and visit => http://127.0.0.1:{}".format(port))
    print("To exit, press ctrl + c")
    print()

    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.call(cmd, stdout=devnull, stderr=devnull)
    except (KeyboardInterrupt, SystemExit):
        print(" Bye!")
