import socket
# Consts
addr_server = '127.0.0.1', 1244
# Создание сетевого сокета
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Указывает адрес сервера и его порт
tcp_socket.bind(addr_server)
# Длина очереди соединения
tcp_socket.listen(2)
# Основной процесс сервера
while True:
	# Создание соединения с клиентом
	connect, addres = tcp_socket.accept()
	print("Accept {}:{}".format(addres[0], addres[1]))
	while True:
		data = connect.recv(1024)
		if not data: break
		else: print("Message:", str(data, "utf-8"))
		connect.send(data)
	connect.close()
