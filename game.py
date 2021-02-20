# Tic Tac Toe game with GUI 
# using tkinter 

# importing all necessary libraries 
import random 
import tkinter 
from tkinter import *
from functools import partial 
from tkinter import messagebox 
from copy import deepcopy 



# sign variable to decide the turn of which player 
COLORS = {'O': "yellow", "X": "green", "origin": "gray"}
sign = 0
SIZE = 15
INFINITE = 10000000
WIN = SIZE if SIZE < 5 else 5
WIDTH_BTN = 3
HEIGHT_BTN = 2

# 3'x' < 'oo'
# 'xx' + 2'x' < 2'xx'
#  '000' > 2'xxx' + 2'xx'
"""
chiến lược tấn công:
giả sử ta đi 'o' dối thủ đi 'x'

+, 2'00' > 3'0' nuoc doi
+, 2'oo' > '00' + 2'o'

->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'00' > 2'0'
'000' >= 2'00' +  2'0'

chiến lược phòng ngự:
2'xx' > 'xx' + 2'x'
2'xx' > 3'x'
->>..........................................'xx' > 2'x'
'ooo' > 3'xx'
'oo' > 2'xx'
3'oo' < 'xxx'# invalid
"""

ATTRACT_CORES = (0, 13, 30, 75,INFINITE + 1, INFINITE, INFINITE)
DEFENCE_CORES = (0, 6, 18, 65,INFINITE, INFINITE, INFINITE)

# Creates an empty board 
global board 
board = [[" " for x in range(SIZE)] for y in range(SIZE)] 

	
# Check l(O/X) won the match or not 
# according to the rules of the game 
def winner(board, tic): 
    way1 = tic * WIN
    way2 = "test"#(l * (WIN - 1)).center(WIN + 1)
    line = ''
    # ckeck rows
    for i in board:
        line = "".join(i)
        if way1 in line or way2 in line:
            return True
    # check colum
    for i in range(SIZE):
        l = [board[j][i] for j in range(SIZE)]
        line = "".join(l)
        if way1 in line or way2 in line:
            return True
    # check diagonal
    i = 0
    while i <= (SIZE - WIN):
        # diagonal top left
        l = [board[j][i + j] for j in range(SIZE - i)]
        line = "".join(l)
        if way1 in line or way2 in line:
            return True
        # diagonal top right
        l = [board[j][SIZE - 1 - i - j] for j in range(SIZE - i)]
        line = "".join(l)
        if way1 in line or way2 in line:
            return True

       
        l = [board[i + j][j] for j in range(SIZE - i)]
        line = "".join(l)
        if way1 in line or way2 in line:
            return True
        
        l = [board[i + j][SIZE - 1 - j] for j in range(SIZE - i)]
        line = "".join(l)
        if way1 in line or way2 in line:
            return True
        i += 1
    return False

# Configure text on button while playing with another player 
def get_text(i, j, gb, l1, l2): 
	global sign 
	if board[i][j] == ' ': 
		if sign % 2 == 0: 
			l1.config(state=DISABLED) 
			l2.config(state=ACTIVE) 
			board[i][j] = "X"
		else: 
			l2.config(state=DISABLED) 
			l1.config(state=ACTIVE) 
			board[i][j] = "O"
		sign += 1
		button[i][j].config(text=board[i][j], bg=COLORS[board[i][j]]) 
	if winner(board, "X"): 
		# gb.destroy() 
		box = messagebox.showinfo("Winner", "Player 1 won the match") 
	elif winner(board, "O"): 
		# gb.destroy() 
		box = messagebox.showinfo("Winner", "Player 2 won the match") 
	elif(isfull(board)): 
		# gb.destroy() 
		box = messagebox.showinfo("Tie Game", "Tie Game") 

# Check if the player can push the button or not 
def isfree(i, j): 
	return board[i][j] == " "

# Check the board is full or not 
def isfull(board): 
    for l in board:
        for i in l:
            if i == " ":
                return False
            
    return True

# Create the GUI of game board for play along with another player 
def gameboard_pl(game_board, l1, l2): 
	global button 
	button = [] 
	for i in range(SIZE): 
		m = 5 + i 
		button.append(i) 
		button[i] = [] 
		for j in range(SIZE): 
			n = j 
			button[i].append(j) 
			get_t = partial(get_text, i, j, game_board, l1, l2) 
			button[i][j] = Button( 
				game_board, bd=3, command=get_t, height = HEIGHT_BTN, width = WIDTH_BTN) 
			button[i][j].grid(row=m, column=n) 
	game_board.mainloop() 

def free_around(i, j):
	rs = 0
	start = 1 - WIN
	for m in range(start, WIN):
		for n in range(start, WIN):
			if (0 <= i + m < SIZE) and (0 <= j + n < SIZE):
				let = board[i + m][j + n]
				if let == " ":
					rs += 1
				elif let == "O":
					rs += 2
	return rs

# AI region
# def minimax(board, max_depth, tic, depth):

# 	if winner(board, tic):
# 		return 9999999
	
# 	if depth == max_depth:
# 		return 

def competiorOf(tic):
	return "X" if tic == "O" else "O"

def attractHorizontial(board, i, j, tic):
	allies, competiors = 0, 0
	let = ''
	
	# horizontial right
	k = 1
	while k + j < SIZE and k < WIN:
		let = board[i][j + k]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
		elif let == competiorOf(tic):
			competiors += 1
			break
		k += 1

	# horizontial left
	
	k = 1
	while j - k >= 0 and k < WIN:
		if(board[i][j - k] == tic):
			allies += 1
		elif board[i][j - k] == competiorOf(tic):
			competiors += 1
			break
		else:
			break
		k += 1
	if (competiors == 2):
		return 0

	if allies > 0 and allies != WIN - 1:
		allies -= competiors

	return ATTRACT_CORES[allies]

def attractVertical(board, i, j, tic):
	allies = 0
	competiors = 0
	let = ''
	# vertical down
	k = 1
	while k + i < SIZE and k <= WIN:
		let = board[i + k][j]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
		elif let == competiorOf(tic):
			competiors += 1
			break
		k += 1
	# vertical up
	
	k = 1
	while i - k >= 0 and k < WIN:
		let = board[i - k][j]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
		elif let == competiorOf(tic):
			competiors += 1
			break
		k += 1

	if (competiors == 2):
		return 0
	if allies > 0 and allies != WIN - 1:
		allies -= competiors
	return ATTRACT_CORES[allies]

def attractDiagonal(board, i, j, tic):
	scores = 0
	allies = 0
	competiors = 0
	let = ''
	
	# dong nam
	k = 1
	while k + i < SIZE and k + j < SIZE and k < WIN:
		let = board[i + k][j + k]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
		elif let == competiorOf(tic):
			competiors += 1
			break
		k += 1

	# tay bac
	k = 1
	
	while j - k >= 0 and i - k >= 0 and k <= WIN:
		let = board[i - k][j - k]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
		elif let == competiorOf(tic):
			competiors += 1
			break
		k += 1

	if not (competiors == 2):
		if allies > 0 and allies != WIN - 1:
			allies -= competiors
		scores += ATTRACT_CORES[allies]
	##################################################
	allies = 0
	competiors = 0
	
	# dong bac
	
	k = 1
	while i - k >= 0 and k + j < SIZE and k <= WIN:
		let = board[i - k][j + k]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
		elif let == competiorOf(tic):
			competiors += 1
			break
		k += 1

	# tay nam
	k = 1
	while j - k >= 0 and i + k < SIZE and k <= WIN:
		let = board[i + k][j - k]
		if(let == tic):
			allies += 1
		elif let == competiorOf(tic):
			competiors += 1
			break
		else:
			break
		k += 1
	if not (competiors == 2):# neu khong bi chan o hay dau
		if allies > 0 and allies != WIN - 1:
			allies -= competiors
		scores += ATTRACT_CORES[allies]
	if scores != 0:
		scores += 1 # uu tien duong cheo
	return scores
######################################### DEFENCE ###############################
def defenceHorizontial(board, i, j, tic):
	allies, competiors = 0, 0
	scores = 0
	let = ''
	oponent = competiorOf(tic)
	# horizontial right
	k = 1
	while k + j < SIZE and k < WIN:
		let = board[i][j + k]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
			break
		elif let == oponent:
			competiors += 1
		k += 1

	# horizontial left
	k = 1
	while j - k >= 0 and k <= WIN:
		let = board[i][j - k]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
			break
		elif let == oponent:
			competiors += 1
		k += 1

	if (allies == 2):
		return 0 # da duoc chan
	if competiors != WIN - 1 and competiors > 0:
		competiors -= allies
	scores += DEFENCE_CORES[competiors]

	return scores


def defenceVertical(board, i, j, tic):
	allies, competiors = 0, 0
	scores = 0	
	let = ''
	oponent = competiorOf(tic)
	# vertical down
	k = 1
	while k + i < SIZE and k < WIN:
		let = board[i + k][j]
		if let == " ":
			break
		if(let == tic):
			allies += 1
			break
		elif let == oponent:
			competiors += 1
		k += 1

	# vertical up
	k = 1
	while i - k >= 0 and k < WIN:
		let = board[i - k][j]
		if let == " ":
			break
		if(let == tic):
			allies += 1
			break
		elif let == oponent:
			competiors += 1
		
		k += 1
	
	if (allies == 2):
		return 0 # neu da chan roi thi thoi
	
	if competiors != WIN - 1 and competiors > 0:
		competiors -= allies
	scores+= DEFENCE_CORES[competiors]
	
	return scores 

def defenceDiagonal(board, i, j, tic):
	allies, competiors = 0, 0
	let = ''
	scores = 0
	oponent = competiorOf(tic)
	# dong nam
	k = 1
	while k + i < SIZE and k + j < SIZE and k < WIN:
		let = board[i + k][j + k]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
			break
		elif let == oponent:
			competiors += 1
		k += 1
	# tay bac
	k = 1
	
	while j - k >= 0 and i - k >= 0 and k < WIN:
		let = board[i - k][j - k]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
			break
		elif let == oponent:
			competiors += 1
		k += 1

	if not (allies == 2):
		if competiors != WIN - 1 and competiors > 0:
			competiors -= allies
		scores += DEFENCE_CORES[competiors] # neu chua chan thi cong diem
	##################################################
	allies = 0
	competiors = 0
	# dong bac
	
	k = 1
	while i - k >= 0 and k + j < SIZE and k < WIN:
		let = board[i - k][j + k]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
			break
		elif let == oponent:
			competiors += 1
			
		k += 1
	# tay nam
	k = 1
	
	while j - k >= 0 and i + k < SIZE and k < WIN:
		let = board[i + k][j - k]
		if let == " ":
			break
		elif(let == tic):
			allies += 1
			break
		elif let == oponent:
			competiors += 1
			
		k += 1

	if not (allies == 2):
		if competiors != WIN - 1 and competiors > 0:
			competiors -= allies
		scores += DEFENCE_CORES[competiors] # neu chua chan thi cong diem
	
	if scores != 0:
		scores += 1 # uu tien duong cheo
	return scores

		
def evaluate(board, i, j, tic):
	ah = attractHorizontial(board, i, j, tic)
	av = attractVertical(board, i, j, tic)
	ad = attractDiagonal(board, i, j, tic) 

	dh = defenceHorizontial(board, i, j, tic)
	dv = defenceDiagonal(board, i, j, tic)
	dd = defenceVertical(board, i, j, tic)

	# win = ATTRACT_CORES[3]
	
	# self_win = ah >= win or av >= win or ad >= win
	# if self_win:
	# 	print("self win")
	# 	return INFINITE
	
	# win = DEFENCE_CORES[3]
	# completior_win = dh >= win or dv >= win or dd >= win
	
	# if completior_win:
	# 	print("completior_win")
	# 	return INFINITE
	
	# # nuoc doi
	# high = ATTRACT_CORES[2]
	# h = ah >= high
	# v = av >= high
	# d = ad >= high
	# self_double_kill = (h and (v or d)) or (d and v) 
	# if self_double_kill:
	# 	print("self_double_kill")
	# 	return INFINITE
	
	# high = DEFENCE_CORES[2]
	# h = dh >= high
	# v = dv >= high
	# d = dd >= high
	# competior_double_kill = (h and (v or d)) or (d and v)
	
	# if competior_double_kill:
	# 	print("competior_double_kill")
	# 	return INFINITE
	
	return max(ah + av + ad, dh + dv + dd)

# Decide the next move of system 
def pc(board): 
	max_core = 0
	best_move = [0, 0]
	for i in range(SIZE): 
		for j in range(SIZE): 
			if board[i][j] == " ": 
				p = evaluate(board, i, j, "O")
				if p > max_core or ((p == max_core) and free_around(i, j) > free_around(best_move[0], best_move[1])):
					max_core = p
					best_move[0] = i
					best_move[1] = j
				
	print(max_core, best_move, "####################")
	return best_move

# Configure text on button while playing with system 
def get_text_pc(i, j, gb, l1, l2): 
	global sign 
	if board[i][j] == ' ': 
		if sign % 2 == 0: 
			l1.config(state=DISABLED) 
			l2.config(state=ACTIVE) 
			board[i][j] = "X"
		else: 
			button[i][j].config(state=ACTIVE) 
			l2.config(state=DISABLED) 
			l1.config(state=ACTIVE) 
			board[i][j] = "O"
		sign += 1
		button[i][j].config(text=board[i][j], bg=COLORS[board[i][j]]) 
	x = True
	if winner(board, "X"): 
		# gb.destroy() 
		x = False
		box = messagebox.showinfo("Winner", "Player won the match") 
	elif winner(board, "O"): 
		# gb.destroy() 
		x = False
		box = messagebox.showinfo("Winner", "Computer won the match") 
	elif(isfull(board)): 
		# gb.destroy() 
		x = False
		box = messagebox.showinfo("Tie Game", "Tie Game") 
	if(x): 
		if sign % 2 != 0: 
			move = pc(board) 
			button[move[0]][move[1]].config(state=DISABLED, bg = COLORS[board[i][j]]) 
			get_text_pc(move[0], move[1], gb, l1, l2) 

# Create the GUI of game board for play along with system 
def gameboard_pc(game_board, l1, l2):
	newgcmd = partial(new_game, game_board)
	newg = Button(game_board, text="New", width = WIDTH_BTN, command = newgcmd) 
	newg.grid(row=0, column=SIZE -1) 
	quit_game = partial(exit, game_board)

	quit_this_game =  Button(game_board, text="Exit", width = WIDTH_BTN, command = quit_game) 
	quit_this_game.grid(row=0, column=SIZE - 2) 
	global button 
	button = [] 
	for i in range(SIZE): 
		m = 5 + i 
		button.append(i) 
		button[i] = [] 
		for j in range(SIZE): 
			n = j 
			button[i].append(j) 
			get_t = partial(get_text_pc, i, j, game_board, l1, l2) 
			button[i][j] = Button( 
				game_board, bd=1, command=get_t, height = HEIGHT_BTN, width = WIDTH_BTN) 
			button[i][j].grid(row=m, column=n) 
	game_board.mainloop() 

def new_game(game_board):
	global sign
	sign = 0
	for i in range(SIZE):
		for j in range(SIZE):
			board[i][j] = ' '
			button[i][j].config(text=" ", state=ACTIVE, bg = COLORS["origin"])

def exit(game_board):
	new_game(game_board)
	game_board.destroy()
	play()

# Initialize the game board to play with system 
def withpc(game_board): 
	game_board.destroy() 
	game_board = Tk() 
	game_board.title("Tic Tac Toe") 
	l1 = Button(game_board, text="P: X", width = WIDTH_BTN) 
	COLORS["origin"] = l1.cget("background")
	print(COLORS["origin"])
	l1.grid(row=0, column=1)
	l2 = Button(game_board, text = "Com: O", 
				width = WIDTH_BTN, state = DISABLED) 
	l2.grid(row = 0, column = 2) 
	gameboard_pc(game_board, l1, l2) 



# Initialize the game board to play with another player 
def withplayer(game_board): 
	game_board.destroy() 
	game_board = Tk() 
	game_board.title("Tic Tac Toe") 
	l1 = Button(game_board, text = "Player 1 : X", width = WIDTH_BTN) 
	
	l1.grid(row = 1, column = 1) 
	l2 = Button(game_board, text = "Player 2 : O", 
				width = WIDTH_BTN, state = DISABLED) 
	
	l2.grid(row = 0, column = 1) 
	gameboard_pl(game_board, l1, l2) 

# main function 
def play(): 
	menu = Tk() 
	menu.geometry("360x360") 
	menu.title("Tic Tac Toe") 
	wpc = partial(withpc, menu) 
	wpl = partial(withplayer, menu) 
	
	head = Button(menu, text = "---Welcome to tic-tac-toe---", 
				activeforeground = 'red', 
				activebackground = "yellow", bg = "red", 
				fg = "yellow", width = 500, font = 'summer', bd = 5) 
	
	B1 = Button(menu, text = "Single Player", command = wpc, 
				activeforeground = 'red', 
				activebackground = "yellow", bg = "red", 
				fg = "yellow", width = 500, font = 'summer', bd = 5) 
	
	B2 = Button(menu, text = "Multi Player", command = wpl, activeforeground = 'red', 
				activebackground = "yellow", bg = "red", fg = "yellow", 
				width = 500, font = 'summer', bd = 5) 
	
	B3 = Button(menu, text = "Exit", command = menu.quit, activeforeground = 'red', 
				activebackground = "yellow", bg = "red", fg = "yellow", 
				width = 500, font = 'summer', bd = 5) 
	head.pack(side = 'top') 
	B1.pack(side = 'top') 
	B2.pack(side = 'top') 
	B3.pack(side = 'top') 
	menu.mainloop() 

# Call main function 
if __name__ == '__main__': 
	play() 
