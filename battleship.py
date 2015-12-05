#!/usr/bin/python

import socket
import sys

class BoardSpot:
	UNKNOWN = '?'
	HIT = 'X'
	MISS = 'O'
	SHIP = 'S'

def main():
	maxHits = 14
	enemyHits = 0
	myHits = 0

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

	if host:
		while(enemyHits < maxHits and myHits < maxHits):
			userX, userY = raw_input("Please input an (X, Y) point in this format: X SPACE Y:\n").split()
			
			userX = int(userX)
			userY = int(userY)

			hit = guess(connection, userX, userY)
			if hit:
				myHits += 1
				enemyBoard[userX][userY] = BoardSpot.HIT
			else:
				enemyBoard[userX][userY] = BoardSpot.MISS

			print "Enemy's Board"
			printBoard(enemyBoard)

			xCoord, yCoord = receiveGuess(connection)
			hit = processGuess(myBoard, int(xCoord), int(yCoord))
			answerGuess(connection, hit)

			print "My Board"
			printBoard(myBoard)

			if hit:
				enemyHits += 1
	else:
		while(enemyHits < maxHits and myHits < maxHits):
			xCoord, yCoord = receiveGuess(connection)
			hit = processGuess(myBoard, int(xCoord), int(yCoord))
			answerGuess(connection, hit)

			print "My Board"
			printBoard(myBoard)

			if hit:
				enemyHits += 1

			userX, userY = raw_input("Please input an (X, Y) point in this format: X SPACE Y:\n").split()
			
			userX = int(userX)
			userY = int(userY)

			hit = guess(connection, userX, userY)
			if hit:
				myHits += 1
				enemyBoard[userX][userY] = BoardSpot.HIT
			else:
				enemyBoard[userX][userY] = BoardSpot.MISS

			print "Enemy's Board"
			printBoard(enemyBoard)

	print "GAME OVER"
	if enemyHits >= maxHits:
		print "You LOST!"
	else:
		print "You WON!"

	connection.close()

def guess(connection, xCoord, yCoord):
	connection.send(str(xCoord) + " " + str(yCoord))
	return receiveAnswer(connection)

def receiveAnswer(connection):
	answer = connection.recv(1)
	if answer == 'H':
		return True
	else:
		return False

def answerGuess(connection, hit):
	if hit:
		connection.send('H')
	else:
		connection.send('M')

def receiveGuess(connection):
	xCoord, yCoord = connection.recv(3).split()
	return xCoord, yCoord

def processGuess(board, xCoord, yCoord):
	hit = False
	if board[xCoord][yCoord] == BoardSpot.SHIP:
		board[xCoord][yCoord] = BoardSpot.HIT
		hit = True
	else:
		board[xCoord][yCoord] = BoardSpot.MISS

	return hit 

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

		placeShip(myBoard, 5-x, int(xcoord), int(ycoord), int(direction))

	return (myBoard, enemyBoard)

def printBoard(board):
	for x in board:
		for y in x:
			print y, " ",
		print "\n"

def placeShip(board, shipSize, xcoord, ycoord, direction):
	
	board[xcoord][ycoord] = BoardSpot.SHIP

if __name__ == '__main__':
	main()