#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import gethostbyname, gethostname

'''Module for the working with stdout'''

def print_host_information(dicts):
    '''This function output information about server.'''
    start = "|--------------------HostInformation--------------------|"
    end = "|-------------------------------------------------------|"
    print(start)
    for field in dicts.keys():
        output = '|' + field + ": " + repr(dicts[field])
        output = output + ' '*(len(end) - len(output) - 1) + '|'
        print(output)
    print(end)

def print_list_users(users):
    '''This function output list users.'''
    end = '|------------------------|'
    start = end + '\n|NAME--------IP----------|'
    print(start)
    for field in users:
        string = '|' + field[0] + ' '*(12 - len(field[0])) + field[1] + ' '*(12 - len(field[1])) + '|'
        print(string)

def is_user():
    res = input("Do you have account?(y|n): ").lower()
    if res == "y" or res == "yes" or res == "да" or res == "д":
        return True
    elif res == "n" or res == "no" or res == "н" or res == "нет":
        return False
    else:
        is_user()

def quiting():
    raise SystemExit

def sign_in():
    """Формирует запрос на авторизацию."""
    print("Sign in:")
    name = input("Please, input your name: ")
    password = input("Please, input your password: ")
    ip_addr = gethostbyname(gethostname())
    return "signin:" + name + "&" + password + "&" + ip_addr

def sign_up():
    """Формирует запрос на регистарцию."""
    print("Sign up:")
    name = input("Please, input your name: ")
    password = input("Please, input your password: ")
    ip_addr = gethostbyname(gethostname())
    return "signup:" + name + "&" + password + "&" + ip_addr

def sign_up_is_successful(name, ip, port):
    print("Sing up is successful!")
    print("User is {} from {}:{}".format(name, ip, port))

def doyouwant(string, func, *args):
    res = input(string).lower()
    if res == "y" or res == "yes" or res == "да" or res == "д":
        if not args: func()
        else: func(*args)
        return True
    elif res == "n" or res == "no" or res == "н" or res == "нет":
        return False
    else:
        doyouwant(string, func, *args)

if __name__ == '__main__':
    pass
