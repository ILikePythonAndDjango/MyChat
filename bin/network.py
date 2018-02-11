#!/usr/bin/python
# -*- coding: utf-8 -*-

from Crypto.Cipher import DES

'''Module for the working with network.'''

# Крипто-ключ
key = b'asdfjkl;'

def pad(text):
    while len(text) % 8 != 0:
        text += b' '
    return text

des = DES.new(key, DES.MODE_ECB)

def request(socket, data, servs, apps):
    '''Sending a request.'''
    data = des.encrypt(pad(data))
        
    socket.connect((servs.ip_addr, apps.tcp_port))
    socket.send(data)
    response = socket.recv(apps.stock_size_message)
    socket.close()
    return response

def waiting_response(socket, size_message, res=b''):
    '''Waiting a reaponse.'''
    data = socket.recv(size_message)
    data = des.decrypt(data)
    if data: res = b"200"
    else: res = b'400'
    socket.send(res)
    return data

if __name__ == '__main__':
    pass
