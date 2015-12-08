#!/usr/bin/python

import socket
import sys

#Class for the game board. Allows for the display of both players' ships
class BoardSpot:
	UNKNOWN = '?'
	HIT = 'X'
	MISS = 'O'
	SHIP = 'S'

#Main function for the game. Controls player connections and game flow. Also contains the victory condition.
def main():
	maxHits = 14
	enemyHits = 0
	myHits = 0

	#Battleship.py must be run with the specified parameters
	#Otherwise, the program will exit
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

	#setup the boards
	#myBoard is the board with the user's ships on it
	#enemyBoard is the board the user will use to target the enemy's ships
	myBoard, enemyBoard = setupBoard()

	#if the user is not the host, they will wait for the host to make the first move
	if host == False:
		xCoord, yCoord = receiveGuess(connection)
		hit = processGuess(myBoard, int(xCoord), int(yCoord))
		answerGuess(connection, hit)

		print "My Board"
		printBoard(myBoard)
		print "The enemy guessed (", xCoord, ", ", yCoord, ")" 

		if hit:
			enemyHits += 1
			print "The enemy hit one of your ships!"
		else:
			print "The enemy missed."

	#if the user is the host, they guess first
	#the main control flow is guess, update board, wait for enemy guess, answer, update board, repeat
	while(enemyHits < maxHits and myHits < maxHits):
		userX, userY = raw_input("Please input an (X, Y) point in this format: X [SPACE] Y:\n").split()
		
		userX = int(userX)
		userY = int(userY)

		hit = guess(connection, userX, userY)
		if hit:
			myHits += 1
			enemyBoard[userX][userY] = BoardSpot.HIT
			print "You hit a ship!"
		else:
			enemyBoard[userX][userY] = BoardSpot.MISS
			print "You missed."

		print "Enemy's Board"
		printBoard(enemyBoard)

		xCoord, yCoord = receiveGuess(connection)
		hit = processGuess(myBoard, int(xCoord), int(yCoord))
		answerGuess(connection, hit)

		print "My Board"
		printBoard(myBoard)

		if hit:
			enemyHits += 1

	print "GAME OVER"
	if enemyHits >= maxHits:
		print "You LOST!"
	else:
		print "You WON!"

	connection.close()

#Function for player to guess at enemy ship location
def guess(connection, xCoord, yCoord):
	connection.send(str(xCoord) + " " + str(yCoord))
	return receiveAnswer(connection)

#Receives hit answer.
#Returns true if a hit, false if a miss
def receiveAnswer(connection):
	answer = connection.recv(1)
	if answer == 'H':
		return True
	else:
		return False

#Sends hit answer, "H" for a hit, "M" for a miss
def answerGuess(connection, hit):
	if hit:
		connection.send('H')
	else:
		connection.send('M')

#Receives the guess. Returns the guess coordinates
def receiveGuess(connection):
	xCoord, yCoord = connection.recv(3).split()
	return xCoord, yCoord

#Checks the guess against the targetted board. Sets a spot to "H" if hit and returns true.
def processGuess(board, xCoord, yCoord):
	hit = False
	if board[xCoord][yCoord] == BoardSpot.SHIP:
		board[xCoord][yCoord] = BoardSpot.HIT
		hit = True
	else:
		board[xCoord][yCoord] = BoardSpot.MISS

	return hit 

#Sets up the host's connection
def setupHost(port):
	hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hostSocket.bind(('0.0.0.0', port))

	hostSocket.listen(1)

	connection, address = hostSocket.accept()

	return connection

#Sets up the connection for the non-host player
def setupClient(host, port):
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((host, port))

	return clientSocket
	
#Initializes the boards and asks the players to set their ships. If invalid coordinates are used, asks them again
def setupBoard():
	myBoard = [[BoardSpot.UNKNOWN for x in range(10)] for x in range(9)]
	enemyBoard = [[BoardSpot.UNKNOWN for x in range(10)] for x in range(9)]

	ships = ["Aircraft Carrier", "Battleship", "Destroyer", "Patrol Boat"]

	for x in range(len(ships)):
		print "Where and in what direction would you like to put your", ships[x], ", which has", 5-x, "spaces?"
		userInput = raw_input("Please enter the X-coordinate, Y-coordinate, and direction in this format: X Y D\n")

		xcoord, ycoord, direction = userInput.split()

		#Should check both x- and y-coordinates to make sure the ship being placed doesn't go off the board
		if (direction == 0)
			if ((xcoord + 5-x > 9) || (xcoord < 0) || (ycoord < 0) || (ycoord > 9))
				print "Insufficient Space, please re-enter coordinates."
				x-=1
			else
				placeShip(myBoard, 5-x, int(xcoord), int(ycoord), int(direction))
		elif (direction == 1)
			if ((xcoord - 5-x < 0) || (xcoord > 9) || (ycoord > 9) || (ycoord < 0))
				print "Insufficient Space, please re-enter coordinates."
				x-=1
			else
				placeShip(myBoard, 5-x, int(xcoord), int(ycoord), int(direction))
		elif (direction == 2)
			if ((ycoord - 5-x < 0) || (ycoord > 9) || (xcoord < 0) || (xcoord > 9))
				print "Insufficient Space, please re-enter coordinates."
				x-=1
			else
				placeShip(myBoard, 5-x, int(xcoord), int(ycoord), int(direction))
		elif (direction == 3)
			if ((xcoord > 9) || (xcoord < 0) || (ycoord < 0) || (ycoord + 5-x > 9))
				print "Insufficient Space, please re-enter coordinates."
				x-=1
			else
				placeShip(myBoard, 5-x, int(xcoord), int(ycoord), int(direction))
		else
			print "Invalid coordinates, please try again.\n"
			x-=1

	return (myBoard, enemyBoard)

#Display the current board
def printBoard(board):
	for x in board:
		for y in x:
			print y, " ",
		print "\n"

#Places the ship onto user's desired position
def placeShip(board, shipSize, xcoord, ycoord, direction):
	
	i = 0
	if (direction == 0)
		for i < shipSize
			board[xcoord + i][ycoord] = BoardSpot.SHIP
	elif (direction == 1)
		for i < shipSize
			board[xcoord - i][ycoord] = BoardSpot.SHIP
	elif (direction == 2)
		for i < shipSize
			board[xcoord][ycoord + i] = BoardSpot.SHIP
	else
		for i < shipSize
			board[xcoord][ycoord - i] = BoardSpot.SHIP

if __name__ == '__main__':
	main()
