#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import socket
import time
from threading import Thread
import bin.output as op
import bin.network as network
from bin.settings import *
from bin.protocol import ServerSession

Server = ServerSettings()
Client = ClientSettings()
Application = ApplicationSettings()

def cheking():
    '''Проверка наличия аккаунта у пользователя'''
    if op.is_user():
        res = op.sign_in()
    else:
        res = op.sign_up()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = network.request(s, res.encode(Application.char_set), Server, Application)
    if res == b'201':
        print("Sign up is successful!")
    elif res == b'202':
        print("Sign in is successful!")
    else:
        print("Error!")

    del s

def client_session():
    """Cессия клиента"""
    cheking()
    for input_line in sys.stdin:
        input_line = "message:" + input_line.strip()
        data = input_line.encode(Application.char_set)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        response = network.request(sock, data, Server, Application)

        if not response:
            break
        else:
            print("Status code", response.decode(Application.char_set))

try:
    # Сеанс клиента
    input_process = Thread(target=client_session)
    input_process.start()
    input_process.join()

    output_process = Thread(target=ServerSession(Client, Application).start)
    output_process.start()
    output_process.join()

except KeyboardInterrupt:
    print("\nSession is over!")

except ConnectionRefusedError as crerror:
    print("Error:", crerror)
    op.doyouwant("May be continue?(y|n): ", client_session)

finally:
    pass
