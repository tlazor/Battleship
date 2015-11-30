#!/usr/bin/python

import socket
import sys

class BoardSpot:
	UNKNOWN = '?'
	HIT = 'X'
	MISS = 'O'
	SHIP = 'S'

def main():

	if len(sys.argv) == 3:
		connection = setupHost(int(sys.argv[2]))
		host = True
	elif len(sys.argv) == 4:
		connection = setupClient(sys.argv[2], int(sys.argv[3]))
		host = False
	else:
		print "usage: (1) python ", sys.argv[0], " host [port]"
		print "       (2) python ", sys.argv[0], " join [host] [port]"
		sys.exit()

	myBoard, enemyBoard = setupBoard()

	printBoard(myBoard);

	connection.close()

def setupHost(port):
	hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hostSocket.bind(('0.0.0.0', port))

	hostSocket.listen(1)

	connection, address = hostSocket.accept()

	return connection

def setupClient(host, port):
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((host, port))

	return clientSocket

def setupBoard():
	myBoard = [[BoardSpot.UNKNOWN for x in range(9)] for x in range(9)]
	enemyBoard = [[BoardSpot.UNKNOWN for x in range(9)] for x in range(9)]

	ships = ["Aircraft Carrier", "Battleship", "Destroyer", "Patrol Boat"]

	for x in range(len(ships)):
		print "Where and in what direction would you like to put your", ships[x], ", which has", 5-x, "spaces?"
		userInput = raw_input("Please enter the X-coordinate, Y-coordinate, and direction in this format: X Y D\n")

		xcoord, ycoord, direction = userInput.split()

		placeShip(myBoard, 5-x, xcoord, ycoord, direction)

		print xcoord, ycoord, direction

	return (myBoard, enemyBoard)

def printBoard(board):
	for x in board:
		for y in x:
			print y, " ",
		print "\n"

def placeShip(board, shipSize, xcoord, ycoord, direction):
	
	board[x][y] = BoardSpot.SHIP

if __name__ == '__main__':
	main()