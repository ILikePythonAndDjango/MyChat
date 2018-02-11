#! usr/bin/python
# -*- coding: utf-8 -*-

import socket

"""Settings for client and server"""

class ApplicationSettings:

    def __init__(self):
        self.protocol_name = 'tcp'
        self.tcp_port = 8080
        self.char_set = "utf-8"
        self.stock_size_message = 1024*10
        self.default_timeout = socket.getdefaulttimeout()
        self.path_db = 'DB/client_base.sqlite3'

class ServerSettings:

    def __init__(self):
        self.host_name = socket.gethostname()
        self.ip_addr = socket.gethostbyname(self.host_name)
        self.listen_clients = 15
        self.request_size_message = 1024*10
        self.response_size_message = 1024*10

class ClientSettings:

    def __init__(self):
        self.PC_name = socket.gethostname()
        self.listen_clients = 15
        self.ip_addr = socket.gethostbyname(self.PC_name)
        self.request_size_message = 1024*10
        self.response_size_message = 1024*10

if __name__ == '__main__':
    pass
