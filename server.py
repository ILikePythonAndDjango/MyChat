#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
#import socket
import time
from threading import Thread
import bin.output as op
#import bin.network as network
from bin.settings import ServerSettings, ApplicationSettings
from bin.protocol import Protocol, ServerSession

Server = ServerSettings()
Application = ApplicationSettings()


# Outputing information about this host
op.print_host_information({
    "Current hostname": Server.host_name,
    "Server IP number": Server.ip_addr,
    "TCP port": Application.tcp_port,
    "Protocol": Application.protocol_name,
    "Timeout": Application.default_timeout,
})
print("Run server in {}...".format(time.asctime()))

try:
    while 1:
        for i in range(2):
            process = Thread(target=ServerSession(Server, Application).start)
            process.start()
            process.join()

except KeyboardInterrupt:
    print("\nSession is over!")

#finally:
#    sock.close()
