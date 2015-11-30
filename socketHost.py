import socket

def main():
	hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hostSocket.bind((socket.gethostname(), 5010))

	hostSocket.listen(1)

	while 1:
		connection, address = hostSocket.accept()

		data = connection.recv(512)

		if len(data) > 0:
			print "Recieved: ", data
			break

	hostSocket.close()

if __name__ == '__main__':
	main()