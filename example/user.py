import sys
import socket
# Ввод ip-адреса и порта сервера
ip, tcp_port = input("Please, intput ip and tcp-port: ").split()
print("Address: {}:{}".format(ip, tcp_port))
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	# Установка TCP-cоединения
	tcp_socket.connect((ip, int(tcp_port)))
	for input_line_message in sys.stdin:
		input_line_message = input_line_message.rstrip()
		byte_data = input_line_message.encode("utf-8")
		# Отправка сообщения
		tcp_socket.send(byte_data)
		response = tcp_socket.recv(1024)
		print("Result response:", response)
		
except KeyboardInterrupt:
	print("\nChat is close!")

except ConnectionRefusedError:
	print("[Errno 111] Connection refused.")
finally:
	tcp_socket.close()
	print("The end!")
