#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

У этого приложения существует такие виды протоколов:

    1. signin 
        Это протокол авторизаци пользователя. Все параметры перечисляются через '&'.
        ip_addr_client не обязательное поле. 
        signin:<name_client>&<password_client>&<ip_addr_client>
    2. signup
        Это протокол регистрации пользователя. Все параметры перечисляются через '&'.
        signup:<name_client>&<password_client>&<ip_addr_client>
    3. message
        Это протокол отправки сообщений
        message:from=<sender_name>&to=<recipient_name>&<short_text>

    Status code:

        1. 200 - удачная отправка сообщения по протоколу message.
        2. 201 - удачная регистрация.
        3. 202 - удачная аторизация.
        4. 400 - сообщение вообще не удалось отправить.
        5. 401 - не удалось зарегистрироваться
        6. 402 - не удалось авторизоваться
        7. 403 - неизвестный протокол

'''

import re
import time
import socket
#from threading import Thread
from Crypto.Cipher import DES
from bin.db import DBMS
from bin.network import waiting_response, pad, key

online_clients = list()

class ProtocolException(Exception):
    pass

class Protocol(object):

    def __init__(self, sock, apps):
        """Выборочная работа с протоколами."""
        # Ответ клиенту
        self._response = b''

        # Объект для работы с базами данных
        self._dbms = DBMS(apps.path_db)

        # Объект для шифрования данных
        self._des = DES.new(key, DES.MODE_ECB)

        # Результат работы алгоритмов
        self._content = ''

        #self._apps = apps

        # Обработка запроса
        data = self._request_serv(sock, apps.stock_size_message)

        # обработка url
        url = data.decode(apps.char_set)
        pattern = r'(.+):(.*)'
        uri_list = re.findall(pattern, url)
        self.protocol_type = 'message'
        self._options = ''
        self._request_info = None

        if not data:
            self._response = b'400'
        else:
            self.protocol_type = uri_list[0][0]
            self.options = uri_list[0][1]
        
        # Выбор алгоритма
        try:
            self._choice_protocol()
        except ProtocolException as pe:
            print(self.protocol_type, "is", pe)
        finally:
            del self._dbms

        sock.send(self._response)
        
        if isinstance(self._request_info, None):
            raise ProtocolException("Does not have information about request")

    def _session_with_client(self, socket):
        pass

    def _signin(self):
        """This method implements algorithm protocol signup."""
        pattern = r'(.+)&(.+)&([0-9.]+)'
        information = re.findall(pattern, self._options)[0]

        self._request_info = information

    def _signup(self):
        """This method implements algorithm protocol signin."""
        pattern = r'(.+)&(.+)&([0-9.]+)'
        information = re.findall(pattern, self._options)[0]
        self._dbms.add_user(information[0], information[1], information[2])
        if not self._dbms.not_db_Error:
            raise ProtocolException("abourted, because " + self._dbms.error_message)

        self._request_info = information

    def _message(self):
        """This method implements algorithm protocol message."""
        pattern = r'from=(.+)&to=(.+)&(.*)'
        information = re.findall(pattern, self._options)[0]

        self._content = information[2]

        self._request_info = information

    def _request_serv(self, socket, size_message):
        '''Waiting a reaponse.'''
        # Ожидание ответа сервер
        data = socket.recv(size_message)
        # Шифрование данных
        data = self._des.decrypt(data)

        return data

    def _choice_protocol(self):
        '''Choicing protocol algorithm'''
        if self.protocol_type == "signin":
            self._response = b"202"
            self._signin()

        elif self.protocol_type == "signup":
            self._response = b'201'
            self._signup()

        elif self.protocol_type == "message":
            self._response = b'200'
            self._message()

        else:
            self._response = b'403'
            raise ProtocolException("Unknow protocol name.")

    def get_content(self):
        return self._content

    def get_information(self):
        pass

class ServerSession:

    '''Session in server.'''

    def __init__(self, servs, apps):
        '''Making TCP-connection'''
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._servs = servs
        self._apps = apps

        # Set settings
        self._socket.bind((self._servs.ip_addr, self._apps.tcp_port))
        self._socket.listen(self._servs.listen_clients)

    def start(self):
        '''Start session for client.'''
        try:
            while 1:
                # Waiting for connection
                connection, addres = self._socket.accept()
                print("Connection for client in {}.\nClient IP number: {}.\nTCP port: {}.".format(time.asctime(), addres[0], addres[1]))

                # Session with the client
                message_control = Protocol(connection, self._apps)
                message = message_control.get_content()

                if message_control.protocol_type == 'message':
                    print('Message:\n', message)

                connection.close()
        except KeyboardInterrupt:
            print("\nSession is over!")
        finally:
            self._socket.close()