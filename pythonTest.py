import socket

def main():
	socketFD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socketFD.bind(('localhost', 5010))

	data = socketFD.recv(512)

	print "Recieved: ", data

	socketFD.close()

if __name__ == '__main__':
	main()