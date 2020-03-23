import sys
import copy

# TODO is there an easy way, given a state and leftover pieces, to make the recursion end early if one of the pieces doesn't have a place?

finished = False
moves = 0

def color(c):
	if c == 0:
		return '.'
	elif c == 1:
		return 'r'
	elif c == 2:
		return 'g'
	else:
		return 'b'

class Piece:
	def __init__(self, n,e,s,w, num=1):
		self.N = n
		self.E = e
		self.S = s
		self.W = w
		self.num = num
	def __repr__(self):
		return "p*"+str(self.num)+"("+color(self.N)+","+color(self.E)+","+color(self.S)+","+color(self.W)+")"

class State:
	def __init__(self):
		# Create an array of pieces, initially all null pieces
		self.pieces = [Piece(0,2,2,2),Piece(1,0,2,2),Piece(0,0,0,0,2),Piece(1,1,0,0),
			Piece(0,2,1,0),Piece(0,0,2,2),Piece(1,2,0,0),Piece(1,0,0,2),
			Piece(1,1,2,0),Piece(1,0,0,1),Piece(0,0,1,1),Piece(2,0,1,1),
			Piece(2,0,1,0,2),Piece(0,2,0,0,2),
			Piece(0,1,0,2),Piece(0,0,1,0),Piece(2,0,0,0)] # 605m finishes with 819930 tries!
		'''[Piece(3,2,0,1),Piece(1,1,0,2),Piece(0,1,0,0),Piece(0,0,0,1),Piece(1,2,3,0),Piece(0,0,1,2),Piece(0,0,0,0,11),Piece(0,1,1,1),Piece(0,1,0,0),Piece(0,0,0,1)]'''
		self.state = [[None, None, None, None],
				[None, None, None, None],
				[None, None, None, None],
				[None, None, None, None],
				[None, None, None, None],]

def printState(state):
	for row in range(0,5):
		# row 1
		for col in range(0,4):
			entry = state[row][col]
			if entry:
				buf = str(entry.N)
				if entry.N == 0:
					buf = " "
			else:
				buf = " "
			sys.stdout.write("|  %s%s  |" % (buf,buf))
		print ""
		# row 2
		for col in range(0,4):
			entry = state[row][col]
			if entry:
				bufw = str(entry.W)
				bufe = str(entry.E)
				bufm = "X"
				if entry.E == entry.W == 0:
					bufw = " "
					bufm = " "
					bufe = " "
				if bufw == "0":
					bufw = ' '
				if bufe == "0":
					bufe = ' '
			else:
				bufw = " "
				bufe = " "
				bufm = " "
			sys.stdout.write("|%s%s%s%s%s%s|" % (bufw,bufw,bufm,bufm,bufe,bufe))
		print ""
		# row 3
		for col in range(0,4):
			entry = state[row][col]
			if entry:
				buf = str(entry.S)
				if entry.S == 0:
					buf = " "
			else:
				buf = " "
			sys.stdout.write("|  %s%s  |" % (buf,buf))
		print ""
		print "="*(8*4)
	sys.stdout.flush()

def checkBalance(pieces):
	length = 0

	#print pieces
	n,e = 0,0
	for piece in pieces:
		n += (10**(piece.N)-1)*piece.num
		e += (10**(piece.E)-1)*piece.num
		n -= (10**(piece.S)-1)*piece.num
		e -= (10**(piece.W)-1)*piece.num
		length += piece.num

	if length != 20:
		print "Invalid number of pieces!"
		return False
	if n==e==0:
		return True
	return False

def neighbors(state, row, col): # returns the neighbors of a place on the state
	# Get N, E, S, W
	# None means nothing filled in yet, 'blank' means it needs to not connect
	N = 0
	E = 0
	S = 0
	W = 0
	if row > 0:
		N = state[row-1][col].S if state[row-1][col] else None
	if col < 3:
		E = state[row][col+1].W if state[row][col+1] else None
	if row < 4:
		S = state[row+1][col].N if state[row+1][col] else None
	if col > 0:
		W = state[row][col-1].E if state[row][col-1] else None

	return [N, E, S, W]

def chooseMostComplicatedPiece(pieces):
	# first iteration, choose the most complicated piece first
	seen = -1
	index = -1
	x = lambda a: 1 if a != 0 else 0

	for i in range(0, len(pieces)):
		piece = pieces[i]
		count = x(piece.N)+x(piece.E)+x(piece.S)+x(piece.W)
		if count > seen:
			index = i
			seen = count

	#print "complicated piece:", index, pieces[index]

	return index

def startingState(state,pieces):
	print ">>>> Starting State <<<<"
	for row in range(0,5):
		for col in range(0,4):
			entry = pieces[-1]
			if entry.num > 1:
				entry.num -= 1
			else:
				pieces.pop()

			state[row][col] = entry
	printState(state)

def search(state, pieces):
	global finished
	global moves


	#printState(state)

	moves += 1
	if moves % 10000 == 0:
		print '.',
		sys.stdout.flush()

	if finished:
		return False
	#print "$$$$$$$$$$$$$ search with state:"
	#printState(state)
	#print "searching with pieces", pieces

	index = chooseMostComplicatedPiece(pieces)
	piece = pieces[index]
	if piece.num > 1:
		piece.num -= 1
	else:
		pieces.pop(index)

	#print "choosing piece", piece, piece.N, piece.E, piece.S, piece.W
	#print "pieces after the pop() call:", pieces

	possiblePlaces = []

	for row in range(0,5):
		for col in range(0,4):
			# Cant place if there is something there already
			if state[row][col] is not None:
				#print piece, "invalid location due to occupied", "in row/col", row,col
				continue

			# Cant place if hitting the sides with an open piece
			# Can't place if hitting another color or a blank other piece with an open piece
			friends = neighbors(state, row, col)

			if (friends[0] is not None) and piece.N != friends[0]:
				#print piece, "invalid location", row, col, "due to N friend", friends[0]
				continue
			if (friends[1] is not None) and piece.E != friends[1]:
				#print piece, "invalid location", row, col, "due to E friend", friends[1]
				continue
			if (friends[2] is not None) and piece.S != friends[2]:
				#print piece, "invalid location", row, col, "due to S friend", friends[2]
				continue
			if (friends[3] is not None) and piece.W != friends[3]:
				#print piece, "invalid location", row, col, "due to W friend", friends[3]
				continue

			# add up all the connected neighbors
			score = (piece.N==friends[0])*(piece.N+1) + (piece.E==friends[1])*(piece.E+1) + (piece.S==friends[2])*(piece.S+1) + (piece.W==friends[3])*(piece.W+1)

			possiblePlaces.append([score, row, col])

	# sort the possiblePlaces list based on score
	possiblePlaces.sort(reverse=True, key=lambda p : p[0])

	for place in possiblePlaces:
		row = place[1]
		col = place[2]
		# If you can place it, call pick_piece on that new state and pieces
		#print "placing", piece, "into row/col", row, col, "\n"
		newstate = copy.deepcopy(state)
		newstate[row][col] = piece

		if len(pieces) <= 0:
			print "Finished! number of moves:", moves
			finished = True
			printState(newstate)
			return True
		result = search(newstate, copy.deepcopy(pieces))
		if result:
			return True
	
	#print ">>>>> Failed this branch of search!"
	return False

def main():
	s = State()
	print copy.deepcopy(s.state)
	print copy.deepcopy(s.pieces)
	startingState(copy.deepcopy(s.state), copy.deepcopy(s.pieces))
	
	if not checkBalance(s.pieces):
		print "Puzzle not balanced! exiting"
		exit()
	search(s.state, s.pieces)

main()