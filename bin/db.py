#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Workin with database.'''

import sqlite3

class DBMS:
    
    def __init__(self, name_db):
        '''Класс для работы с базами данных'''
        self.name_db = name_db
        self.database = sqlite3.connect(name_db)
        self.cursor = self.database.cursor()
        self.not_db_Error = True
        self.error_message = ''

    def _query(self, sql_string, pr=False):
        '''Метод делает запрос в базу данных'''
        try:
            self.cursor.execute(sql_string)
        except sqlite3.DatabaseError as err:
            self.not_db_Error = False
            self.error_message = err
            print("Database error:", err)
        else:
            if pr: print("The request in {} was successful!".format(self.name_db))
    
    def add_user(self, nick_name, password, ip_addr):
        '''Метод создает нового пользователя в базе данных.'''
        sql_insert = 'INSERT INTO users VALUES ("{}", "{}", "{}");'.format(nick_name, password, ip_addr)
        self._query(sql_insert, True)
        self.database.commit()

        if self.not_db_Error:
            print("Sing up is successful!")
            print("User is {} from {}".format(nick_name, ip_addr))
            return True
        else:
            return False

    def del_user_byname(self, nick_name):
        '''Метод удаляет пользователя из базы данных по его имени'''
        sql_delete = 'DELETE FROM users WHERE nikname = "{}";'.format(nick_name)
        self._query(sql_delete, True)
        self.database.commit()

    def del_user_byip(self, ip_addr):
        '''Метод удаляет пользователя из базы данных по его IP'''
        sql_delete = 'DELETE FROM users WHERE IP = "{}";'.format(ip_addr)
        self._query(sql_delete, True)
        self.database.commit()

    def get_list_users(self):
        '''Метод возврашает список пользователей с их ip аддресами, как итерируемы объект'''
        sql_select = 'SELECT nickname, IP FROM users;'
        self._query(sql_select)
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.database.close()

if __name__ == '__main__':
    pass
