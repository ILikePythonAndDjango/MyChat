import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1234))
s.listen(10)
while True:
	conn, addr = s.accept()
	print("TCP-request is accept: {}:{}".format(addr[0], addr[1]))
	while True:
		data = conn.recv(1024)
		if not data: break
		else: print("Massage: {}".format(str(data, encoding="utf-8")))
		conn.send(data)
	conn.close
