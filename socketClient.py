import socket

def main():
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect(('127.0.0.1', 5010))

	clientSocket.send('I sent this')

if __name__ == '__main__':
	main()