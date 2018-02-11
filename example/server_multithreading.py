# -*- coding: utf-8 -*-
# Реализация многопоточного сервера
import socket
import threading
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 2222))
sock.listen(30)
def tcp_port():
	connect, addres = sock.accept()
	while True:
		data = sock.recv(1024)
		if not data: break
		connect.send(data)
	connect.close()
while True:
	for count in range(10):
		tcp_thread = threading.Thread(target=tcp_port)
		tcp_thread.start()
		tcp_thread.join()
