# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Aidan Waldrop
#               Benjamin Hoang
#               Dylan Knox
#               Dylan Sartain
# Section:      568
# Assignment:   Lab Topic 13 Team Sorry!
# Date:         19 November 2024

from math import *
import random

import pathlib
parent_dir = str(pathlib.Path(__file__).parent.absolute())
file_name = parent_dir + "/sorry_cards.txt"

#Create Board & other variables
# [character, [spot(x,y), spot(x,y), spot(x,y), spot(x,y)] ]
players = {"Player 1": ["",[]], "Player 2": ["",[]], "Player 3": ["",[]], "Player 4": ["",[]]}
origins = [(11,0), (0,4), (4,15), (15,11)]
home = [(13,0),(0,2),(2,15),(15,13)]
home_directions = [[1,0],[0,1],[-1,0],[0,-1]]
turn = 0
board = []

console_msg = "" # the announcement whenever printBoard() is called
file = open(file_name,'r')

for i in range(16):
	board.append(list())
	for j in range(16):
		# board spaces
		if (i==0 or i==15) or (j==0 or j==15) or (j == 2 and 1 <= i <= 6) or (i == 2 and 9 <= j < 15) or (j == 13 and 9 <= i < 15) or (i == 13 and 1 <= j <= 6):
			board[i].append("[ ]")
			
        # empty space
		else:
			board[i].append("   ")


# ================================================================ Display Functions ================================================================

# runs at the beginning of the program
def welcome():
	print("\n\n")
	print("-----" * 30,"\n" * 13)
	print("1. Each player must choose which character they would like to represent their pawns on the game board")
	print("2. Players must hit enter to draw a card")
	print("3. Starting with player 1, each player must draw a 1, 2, or Sorry! card to leave their start zone")
	print("4. Once each player has left their start zone, each card drawn will have different actions associated with them")
	print("5. For cards 1, 2, 3, 5,8, and 12, one pawn just moves forward the number of spaces of the card drawn")
	print("6. For card 4, one pawn will move backward four spaces")
	print("7. For card 7, one pawn can move forward 7 spaces, or 7 forward movements can be spliti between any two pawns")
	print("8. For card 10, one pawn can move forward ten spaces, or can move back one space")
	print("9 For card 11, one pawn can move forward 11 spaces, or one pawn can switch places with an opponents pawn")
	print("10 For a Sorry! Card, one pawn from start can take th e place of an opponents pawn, returning it to start\n")
	
	print("GAME PLAY")
	print("Jumping and Bumping: You can jump over your or an opponent's pawn if still moving forward. However, if landing in a spot with an opponent pawn within, the enemy pawn will move back to start")
	print("Moving backwards: If you have moved a pawn two spcaes beyond your starting point and get a 4 or 10 card, you can just return to your safety area.\n")
    
    
    
    
    
    
    
  
    
	b = input("^^^ Please pull up the terminal window so you can see the line above ^^^\nPress Enter to continue:")
	print("\n\n\n" * 10)
	print("\n\nWelcome!\n\n\n\nAidan Waldrop\nBenjamin Hoang\nDylan Knox\nDylan Sartain\n\n")
	print("\n          Presents\n\n")
	print(" ______________________________ ")
	print("|                              |")
	print("|            Sorry!            |")
	print("|______________________________|")
	a = input("\n" * 8 +"Press Enter to continue:")
	print("\n\n\n" * 10)


# print the board
def printBoard():
	global console_msg
	global turn
	print("\n" * 10 + "   " * 6 + "Sorry!\n")
	print("   " * 5 + "--> --> -->")
	for each in board:
		for space in each:
			print(space,end="")
		print()
	print(f"Turn: Player {turn}" + "     " + "<-- <-- <--\n")
	
	# print the usernames and how many pawns they have in their starting area
	for i in range(2):
		s = f"   Player {i + 1}: {players[f"Player {i + 1}"][0]} " + "*"*(4-len(players[f"Player {i + 1}"][1])) + ("   " * 3)
		s += " " * len(players[f"Player {i + 1}"][1])
		s += f"Player {i + 3}: {players[f"Player {i + 3}"][0]} " + "*"*(4-len(players[f"Player {i + 3}"][1]))
		print(s)
	print("\n" + console_msg)
	console_msg = ""

# ================================================================ Input Functions ================================================================

def askPlayerUser(i):
	'''Ask player i for their username.
	
	Returns a single character.'''

	err_msg = ""
	char = ""
	while char == "":
		# display the characters already selected
		print("\n\n\n" * 10)
		for player in players:
			if players[player][0]:
				print(f"{player}: {players[player][0]}")
		print(err_msg)
		err_msg = ""
		
		# ask the next player for their character
		char = input(f"\nPlayer {i}, enter your character: ")
		for player in players:
			if len(char) != 1:
				err_msg = "Invalid username! Enter a single character."
				char = ""
				break
			elif char == players[player][0]:
				err_msg = "That character is already in use!"
				char = ""
				break
	return char



def askPlayerPawn(i):
	'''Displays player i's pawns and asks which pawn to use.
	
	Returns an int of which pawn to use.
	Returns -1 if the player has no pawns.'''

	answer = ""
	err_msg = ""
	pawns = players[f"Player {i}"][1]
	if len(pawns) < 1:
		return -1
	print("\n\n\n" * 10)

	while answer == "":
		printBoard()
		# give the player the options
		for f, each in enumerate(pawns):
			print(f"Pawn {f + 1}: {each}")
		print(err_msg, "\n")
		err_msg = ""

		# ask the player
		answer = input(f"Player {i}, enter the pawn you would like to move: ")
		try:
			if 0 < int(answer) <= len(pawns):
				print("\n\n\n" * 14)
				return int(answer) - 1
			else:
				err_msg = "Invalid answer! Try again."
		except:
			err_msg = "Invalid answer! Answer with a number."
		answer = ""
		print("\n\n\n" * 6)


def askPlayerMoves(i):
	'''Asks player i how many moves they want to split.
	Used for card 7.
	
	Returns an int of how many moves they want to split.'''

	answer = ""
	err_msg = ""
	print("\n\n\n" * 10)

	while answer == "":
		printBoard()
		print(err_msg)
		err_msg = ""

		# ask the player
		answer = input(f"Player {i}, enter how many spaces you would like to move: ")
		try:
			if 0 < int(answer) <= 6:
				print("\n\n\n" * 14)
				return int(answer) - 1
			else:
				err_msg = "Invalid answer! Try again."
		except:
			err_msg = "Invalid answer! Answer with a number."
		answer = ""
		print("\n\n\n" * 6)


def askPlayerEnemy(i):
	answer = ""
	err_msg = ""
	print("\n\n\n" * 10)
	pawns = players[f"Player {i}"][1]
	
	enemy_player = -1
	enemy_pawn = -1

	while answer == "":
		printBoard()
		print(err_msg)
		err_msg = ""

		# ask the player
		answer = input(f"Player {i}, which player would you like to switch with? ")
		try:
			if 0 < int(answer) <= 4:
				print("\n\n\n" * 14)
				enemy_player = int(answer) 		# returns 1, 2, 3, or 4
				answer = ""
				break
			else:
				err_msg = "Invalid answer! Try again."
		except:
			err_msg = "Invalid answer! Answer with a number."
		answer = ""
		print("\n\n\n" * 6)
		
	while answer == "":
		printBoard()
		print(err_msg)
		err_msg = ""
		
		# give the player the options
		for f, each in enumerate(players[f"Player {enemy_player}"][1]):
			print(f"Pawn {f + 1}: {each}")

		# ask the player
		answer = input(f"Player {i}, which of Player {enemy_player} pawn would you like to switch with? ")
		try:
			if 0 < int(answer) <= len(pawns):
				print("\n\n\n" * 14)
				enemy_pawn = int(answer)
				break
			else:
				err_msg = "Invalid answer! Try again."
		except:
			err_msg = "Invalid answer! Answer with a number."
		answer = ""
		print("\n\n\n" * 6)
	return (enemy_player,enemy_pawn)

# ================================================================ Specific Functions ================================================================

	
def checkHome(i,pawn):
	'''Checks if player i's pawn is in the home stretch.
	
	Returns booleans (isHome, onHomeSpot)'''
	pos = players[f"Player {i}"][1][pawn]
	
	if pos[0] == home[i - 1][0] and pos[1] == home[i - 1][1]:
		return (False, True)
	
	if pos[0] != 15 and pos[0] != 0:
		if pos[1] != 15 and pos[1] != 0:
			return (True, False)
	return (False, False)


def findPlayer(x,y):
	'''finds the number of the player and their pawn at (x,y)
	
	Returns (player,pawn)'''

	for i,player in enumerate(players):
		for j,pawn in enumerate(players[player][1]):
			if pawn[0] == y and pawn[1] == x and players[player][0] in board[y][x]:
				return (i + 1,j)
	return (1,0)


def kickPawn(i,x,y,check = False):
	'''If a spot is occupied, kick that pawn off
	
	i = player number
	x = x position of the occupied spot
	y = y position of the occupied spot

	Returns True if the the pawn was kicked off
	Returns False if the pawn is player i's own pawn'''

	global console_msg
	player,enemy_pawn = findPlayer(x,y)
	if player == i:
		return False
	if not check:
		console_msg += f"Sorry! Player {i} just knocked Player {player}'s pawn #{enemy_pawn + 1} back to their starting area!\n"
		players[f"Player {player}"][1].pop(enemy_pawn)
	return True


def placePawn(i,pawn = 0,spot = None):
	'''Either place a new pawn on its player i's starting area or place an existing pawn onto a specific spot.
	If the spot is already taken, it will kick the pawn off and force it back to the starting area.'''

	global console_msg
	s = f"[{players[f"Player {i}"][0]}]"

	# this is used for taking pawns out of the starting area
	if spot == None:
		# if not empty
		target = board[origins[i-1][0]][origins[i-1][1]]
		if not "[ ]" in target:
			# if the target spot is occupied by another player
			if not players[f"Player {i}"][0] in target:
				kickPawn(i,origins[i-1][0],origins[i-1][1])
			else:
				console_msg += f"Player {i} could not move.\n"
				return
			
		# update the board
		board[origins[i-1][0]][origins[i-1][1]] = s
		# create a position for the pawn
		origin = [origins[i-1][0],origins[i-1][1]]
		
		if pawn != 0:
			players[f"Player {i}"][1][pawn] = origin
			return
		players[f"Player {i}"][1].append(origin)



	# this is used for sorry cards
	if spot != None:
		target = board[spot[0]][spot[1]]
		# if not empty
		if not "[ ]" in target:
			# if the target spot is occupied by another player
			if not players[f"Player {i}"][0] in target:
				currentSpot = players[f"Player {i}"][1][pawn]
				board[spot[0]][spot[1]] = s
				kickPawn(i,spot[1],spot[0])
				board[currentSpot[0]][currentSpot[1]] = "[ ]"
				players[f"Player {i}"][1][pawn] = [spot[0],spot[1]]
				return
			console_msg += f"Player {i} could not move.\n"
		else:
			currentSpot = players[f"Player {i}"][1][pawn]
			board[spot[0]][spot[1]] = s
			board[currentSpot[0]][currentSpot[1]] = "[ ]"
			players[f"Player {i}"][1][pawn] = [spot[0],spot[1]]
		
	return


def move(i,n,p = -1):
	'''Move the pawn n times for player i from its current position.

	p (optional): only for checking if the player can move.'''

	global console_msg
	check = True # the function will only check if the player can move
	pawn = p
	if p < 0:
		check = False
		pawn = askPlayerPawn(i)
	pos = players[f"Player {i}"][1][pawn]
	currentPos = (int(pos[0]),int(pos[1])) # (y,x) Store the current position  (only for check)
	increment = int(n // fabs(n))
	dir = [0,0]

	for h in range(int(fabs(n))):
		# find the direction (yes, all this is necesasary)
		if pos[1] - 1 < 0:
			dir = [0,-1] # up
			if not 0 <= pos[0] - increment <= 15:
				dir = [1 * increment,0]
		elif pos[0] - 1 < 0:
			dir = [1,0] # right
			if not 0 <= pos[1] + increment <= 15:
				dir = [0,1 * increment]
		elif pos[1] + 1 > 15:
			dir = [0,1] # down
			if not 0 <= pos[0] + increment <= 15:
				dir = [-1 * increment,0]
		elif pos[0] + 1 > 15:
			dir = [-1,0] # left
			if not 0 <= pos[1] - increment <= 15:
				dir = [0,-1]
	
		# move inside the home stretch
		isHome, onHomeSpot = checkHome(i,pawn)
		if n > 0:
			if isHome or onHomeSpot:
				dir = home_directions[i - 1]
		elif n < 0 and isHome and not onHomeSpot:
			dir = home_directions[i - 1]

		# move in the direction
		players[f"Player {i}"][1][pawn][1] += dir[0] * increment
		players[f"Player {i}"][1][pawn][0] += dir[1] * increment
	
	y = players[f"Player {i}"][1][pawn][0]
	x = players[f"Player {i}"][1][pawn][1]

	# check if the new spot is taken: if so, then kick that player back to their starting point
	# if the spot is taken by the player's own pawn then return False
	if board[y][x] != "[ ]":
		if not kickPawn(i,x,y,check):
			return False
		
	if not check:
		# move the pawn
		console_msg += f"Player {i}'s pawn #{pawn + 1} moved {n} spots.\n"

		# add the new marker
		board[y][x] = f"[{players[f"Player {i}"][0]}]"

		# remove the old marker
		board[currentPos[0]][currentPos[1]] = "[ ]"
	else:
		pos[0] = currentPos[0]
		pos[1] = currentPos[1]

	return True


def canPlayerMove(i,n):
	'''Checks if player i can move any pawn n times'''

	if len(players[f"Player {i}"][1]) == 0:
		return False
	for j in range(len(players[f"Player {i}"][1])):
		if not move(i,n,j):
			return False
	return True

# ================================================================ Action Functions ================================================================

def newPawn(i,num_pawns):
	'''Will place a new pawn on the player's start point
	
	Returns (err_msg,answer)'''

	#check if there's enough pawns in the start area
	if num_pawns < 4:
		# check if the start point is taken by the player's own pawn
		origin = board[origins[i-1][0]][origins[i-1][1]]
		if not players[f"Player {i}"][0] in origin:
			placePawn(i)
			return ("","done")
		return ("Your start point is taken by your own pawn. Try again.","")
	else:
		return ("There are no more pawns in your start area. Try again.","")
	

def movePawn(i,n,num_pawns):
	'''Moves player i's pawn for n spaces.
	Checks if player i has at least 1 pawn.

	Returns (error message, answer)
	error message : message to display
	answer : if empty, the while loop should be programmed to run again'''

	if num_pawns > 0:
		if move(i,n) == True:
			return ("","done")
		else:
			return ("You cannot bump your own pawn off the board. Try again.", "")
	return ("You need to have at least one pawn on the board. Try again.", "")


def splitPawn(i,num_pawns):
	global console_msg
	'''Allows for player i to split 7 moves into 2 pawns.
	Checks if player i has at least 2 pawns.

	Returns (error message, answer)
	error message : message to display
	answer : if empty, the while loop should be programmed to run again'''

	if num_pawns > 1:
		moves = askPlayerMoves(i)
		console_msg += "Choose which pawn to move first."
		if not move(i,moves):
			return ("You cannot move there. Try again.","")
		console_msg += "Choose the pawn to move second."
		if not move(i,6-moves):
			return ("You cannot move there. Try again.","")
		return ("","done")

	return ("You need to have at least two pawns on the board. Try again.","")
    
def switchPawn(i,kickoff = False):
	global console_msg
	'''Allows to switch places with pawn
	OR kicks a pawn off the board
	
	kickoff : if True, the program will kick off the pawn instead of switching'''
	pawn = askPlayerPawn(i) + 1
	if pawn > 0:
		enemy_player, enemy_pawn = askPlayerEnemy(i)
		enemy_spot = []
		try:
			enemy_spot = list(players[f"Player {enemy_player}"][1][enemy_pawn - 1])
			player_spot = list(players[f"Player {i}"][1][pawn - 1])
		except:
			return ("You cannot switch with the pawn specified. Try again.","")
		if len(enemy_spot) == 0:
			return ("You cannot switch with the pawn specified. Try again.","")
		
        # place player on enemy spot
		board[enemy_spot[0]][enemy_spot[1]] = f"[{players[f"Player {i}"][0]}]"
		players[f"Player {i}"][1][pawn - 1] = enemy_spot
		
        # place enemy on player spot only if kickoff is false
		if not kickoff:
			board[player_spot[0]][player_spot[1]] = f"[{players[f"Player {enemy_player}"][0]}]"
			players[f"Player {enemy_player}"][1][enemy_pawn - 1] = player_spot
			console_msg += f"Sorry! Player {i} just switched places with Player {enemy_player}!\n"
		else:
			board[player_spot[0]][player_spot[1]] = "[ ]"
			players[f"Player {enemy_player}"][1].pop(enemy_pawn - 1)
			console_msg += f"Sorry! Player {i} just kicked Player {enemy_player}'s pawn #{enemy_pawn} off the board!"
		return ("","done")
	return ("You need to have at least one pawn on the board. Try again.","")

# ================================================================ Game Functions ================================================================

def createPieces():
	global console_msg
	for i in range(4):
		players[f"Player {i + 1}"][0] = askPlayerUser(i + 1)
	print("\n\n\n" * 10)
	board[1][4] = " ^ "
	board[2][4] = f" {players['Player 2'][0]} "
	board[11][1] = " < "
	board[11][2] = f"{players['Player 1'][0]}  "
	board[4][14] = " > "
	board[4][13] = f"  {players['Player 3'][0]}"
	board[13][11] = f" {players['Player 4'][0]} "
	board[14][11] = " v "
	console_msg += "Ready to play?\n\n"

def updateTurn():
	global turn

	printBoard()
	if turn == 4:
		turn = 0
	turn += 1
	a = input(f"Player {turn}, your turn. Press Enter to continue.")


# ================================================================ Card Functions ================================================================


def card1():
	'''Draw a 1 card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a 1 card!\n"

	err_msg = ""
	answer = ""
	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Move forward one.\n2. Move a pawn out of the start area.\n3. Skip turn.")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])
		cannotMove = not canPlayerMove(i,1)
		cannotStart = False

		# Move forward 1
		if "1" in answer:
			err_msg, answer = movePawn(i,1,num_pawns)

		# move a pawn out of the start area
		if "2" in answer:
			err_msg, answer = newPawn(i,num_pawns)
			if "" in answer:
				cannotStart = True

		if "3" in answer:
			if cannotMove and cannotStart:
				console_msg += f"Player {i} skipped their turn."
				break
			err_msg = "First, try to move forward or place a pawn on the starting point."
			answer = ""
	return


def card2():
	'''Draw a 2 card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a 2 card!\n"
	err_msg = ""
	answer = ""
	cannotMove = not canPlayerMove(i,2)
	cannotStart = False

	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Move forward two.\n2. Move a pawn out of the start area.\n3. Draw again.")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])

		# Move forward 2
		if "1" in answer:
			if num_pawns > 0:
				if move(i,2) == True:
					break
				else:
					err_msg = "You cannot bump your own pawn off the board. Try again."
			else:
				err_msg = "You need to have at least one pawn on the board. Try again."
			answer = ""

		# move a pawn out of the start area
		if "2" in answer:
			err_msg, answer = newPawn(i,num_pawns)
			if "" in answer:
				cannotStart = True

		# draw again
		if "3" in answer:
			if cannotMove and cannotStart:
				turn -= 1
				console_msg += f"Player {i} drew another card."
				break
			err_msg = "First, try to move forward or place a pawn on the starting point."
			answer = ""
	return


def card3():
	'''Draw a 3 card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a 3 card!\n"
	err_msg = ""
	answer = ""
	cannotMove = not canPlayerMove(i,3)

	if cannotMove:
		printBoard()
		a = input("Sorry! You cannot move. Press Enter to end your turn. ")
		return

	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Move forward three.")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])

		# Move forward 3
		if "1" in answer:
			if num_pawns > 0:
				if move(i,3) == True:
					break
				else:
					err_msg = "You cannot bump your own pawn off the board. Try again."
			else:
				err_msg = "You need to have at least one pawn on the board. Try again."
			answer = ""
	return

def card4():
	'''Draw a 4 card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a 4 card!\n"
	err_msg = ""
	answer = ""
	cannotMove = not canPlayerMove(i,-4)

	if cannotMove:
		printBoard()
		a = input("Sorry! You cannot move. Press Enter to end your turn. ")
		return

	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Move backward four.")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])

		# Move backward 4
		if "1" in answer:
			if num_pawns > 0:
				if move(i,-4) == True:
					break
				else:
					err_msg = "You cannot bump your own pawn off the board. Try again."
			else:
				err_msg = "You need to have at least one pawn on the board. Try again."
			answer = ""
	return

def card5():
	'''Draw a 5 card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a 5 card!\n"
	err_msg = ""
	answer = ""
	cannotMove = not canPlayerMove(i,5)

	if cannotMove:
		printBoard()
		a = input("Sorry! You cannot move. Press Enter to end your turn. ")
		return

	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Move forward five.")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])

		# Move forward 5
		if "1" in answer:
			if num_pawns > 0:
				if move(i,5) == True:
					break
				else:
					err_msg = "You cannot bump your own pawn off the board. Try again."
			else:
				err_msg = "You need to have at least one pawn on the board. Try again."
			answer = ""
	return

def card7():
	'''Draw a 7 card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a 7 card!\n"
	err_msg = ""
	answer = ""
	cannotMove = not canPlayerMove(i,10)

	if cannotMove:
		printBoard()
		a = input("Sorry! You cannot move. Press Enter to end your turn. ")
		return

	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Move forward seven. \n2. Split seven moves between two pawns.")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])

		# Move forward 7
		if "1" in answer:
			if num_pawns > 0:
				if move(i,7) == True:
					break
				else:
					err_msg = "You cannot bump your own pawn off the board. Try again."
			else:
				err_msg = "You need to have at least one pawn on the board. Try again."
			answer = ""
		if "2" in answer:
			err_msg, answer = splitPawn(i,num_pawns)
	return

def card8():
	'''Draw a 8 card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a 8 card!\n"
	err_msg = ""
	answer = ""
	cannotMove = not canPlayerMove(i,8)

	if cannotMove:
		printBoard()
		a = input("Sorry! You cannot move. Press Enter to end your turn. ")
		return

	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Move forward eight.")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])

		# Move forward 8
		if "1" in answer:
			if num_pawns > 0:
				if move(i,8) == True:
					break
				else:
					err_msg = "You cannot bump your own pawn off the board. Try again."
			else:
				err_msg = "You need to have at least one pawn on the board. Try again."
			answer = ""
	return

def card10():
	'''Draw a 10 card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a 10 card!\n"
	err_msg = ""
	answer = ""
	cannotMove = not canPlayerMove(i,10)

	if cannotMove:
		printBoard()
		a = input("Sorry! You cannot move. Press Enter to end your turn. ")
		return

	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Move forward ten. \n2. Move Backwards one")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])

		# Move forward 10
		if "1" in answer:
			if num_pawns > 0:
				if move(i,10) == True:
					break
				else:
					err_msg = "You cannot bump your own pawn off the board. Try again."
			else:
				err_msg = "You need to have at least one pawn on the board. Try again."
			answer = ""
		# Move backward 1
		if "2" in answer:
			if num_pawns > 0:
				if move(i,-1) == True:
					break
				else:
					err_msg = "You cannot bump your own pawn off the board. Try again."
			else:
				err_msg = "You need to have at least one pawn on the board. Try again."
			answer = ""
	return

def card11():
	'''Draw a 11 card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a 11 card!\n"
	err_msg = ""
	answer = ""
	cannotMove = not canPlayerMove(i,11)
	cannotSwitch = True

	if cannotMove:
		printBoard()
		a = input("Sorry! You cannot move. Press Enter to end your turn. ")
		return
    
    # if it finds at least one pawn from another player, it will set cannotSwitch to False
	for index in range(4):
		if index + 1 != i and len(players[f"Player {index + 1}"][1]) > 0:
			cannotSwitch = False
	if len(players[f"Player {i}"][1]) > 0:
		cannotSwitch = False

	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Move forward eleven. \n2. switch with other player's piece.\n3. Skip turn.")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])

		# Move forward 11
		if "1" in answer:
			if num_pawns > 0:
				if move(i,11) == True:
					break
				else:
					err_msg = "You cannot bump your own pawn off the board. Try again."
			else:
				err_msg = "You need to have at least one pawn on the board. Try again."
			answer = ""
		if "2" in answer:
			err_msg, answer = switchPawn(i)
		if "3" in answer:
			if cannotMove and cannotSwitch:
				console_msg += f"Player {i} skipped their turn."
				break
			err_msg = "First, try to switch spots with another player."
			answer = ""
	return

def card12():
	'''Draw a 12 card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a 12 card!\n"
	err_msg = ""
	answer = ""
	cannotMove = not canPlayerMove(i,12)

	if cannotMove:
		printBoard()
		a = input("Sorry! You cannot move. Press Enter to end your turn. ")
		return

	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Move forward twelve.")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])

		# Move forward 12
		if "1" in answer:
			if num_pawns > 0:
				if move(i,12) == True:
					break
				else:
					err_msg = "You cannot bump your own pawn off the board. Try again."
			else:
				err_msg = "You need to have at least one pawn on the board. Try again."
			answer = ""
	return


def sorryCard():
	'''Draw a Sorry card.'''
	global turn
	global console_msg
	i = turn
	console_msg += "You pulled a Sorry card!\n"
	err_msg = ""
	answer = ""
	cannotMove = True
	cannotStart = False
	
    # if it finds at least one pawn from another player, it will set cannotMove to False
	for index in range(4):
		if index + 1 != i and len(players[f"Player {index + 1}"][1]) > 0:
			cannotMove = False
	if len(players[f"Player {i}"][1]) > 0:
		cannotMove = False

	while answer == "":
		print("\n" * 10)
		printBoard()
		print("Options:\n1. Kick another player's pawn off the board.\n2. Move a pawn out of the start area.\n3. Skip turn.")
		print(err_msg)
		answer = input("\nChoose an option: ")
		num_pawns = len(players[f"Player {i}"][1])

		# kick another player off the board
		if "1" in answer:
			err_msg, answer = switchPawn(i,True)
			
		# move a pawn out of the start area
		if "2" in answer:
			err_msg, answer = newPawn(i,num_pawns)
			if "" in answer:
				cannotStart = True
				
		if "3" in answer:
			if cannotMove and cannotStart:
				console_msg += f"Player {i} skipped their turn."
				break
			err_msg = "First, try to switch spots with another player or place a pawn on the starting point."
			answer = ""
	return


def main():
	welcome()
	createPieces()
	printBoard()
	a = input("Press Enter to continue:")
	updateTurn()
	data = file.read().split("\n")
    

	for i in range(100):
		num = data[random.randint(0,44)]
		if num == '1':
			card1()
		elif num == '2':
			card2()
		elif num == '3':
			card3()
		elif num == '4':
			card4()
		elif num == '5':
			card5()
		elif num == '7':
			card7()
		elif num == '8':
			card8()
		elif num == '10':
			card10()
		elif num == '11':
			card11()
		elif num == '12':
			card12()
		elif num == 'sorry':
			sorryCard()
		updateTurn()

main()
file.close()
