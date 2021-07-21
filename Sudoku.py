from random import randint
import copy
import datetime

class Stack:
  def __init__(self):
    self.topOfStack = None

  def isEmpty(self):
    return (self.topOfStack == None)

  def pop(self):
    if(self.isEmpty()):
      return None

    retNode = self.topOfStack
    self.topOfStack = self.topOfStack.prevNode
    return retNode

  def push(self, board):
    self.topOfStack = Node(board, self.topOfStack)

class Node:
  def __init__(self, b, p):
    self.board = copy.deepcopy(b)
    self.prevNode = p

def solvePuzzleDegree(sodukoArray):
  print("solvePuzzleDegree")

  stack = Stack()
  stack.push(sodukoArray)
  while(not stack.isEmpty()):
    currentBoard = stack.pop().board
    #print("pop")

    #fill in any squares with 1 move
    numMoveArray = getNumValuesForEverySquare(currentBoard)
    changeMade = True
    while(changeMade):
      changeMade = False
      for r in range(0, len(currentBoard)):
        for c in range(0, len(currentBoard[r])):
          if (numMoveArray[r][c] == 1):
            changeMade = True
            #print(getPossibleValuesForSquare(currentBoard, r, c))
            currentBoard[r][c] = getPossibleValuesForSquare(currentBoard, r, c)[0]
            numMoveArray = getNumValuesForEverySquare(currentBoard)

    #checks if is solved
    #if(isSolved(currentBoard)):
    #  return currentBoard

    max = -1
    maxRow = -1
    maxCol = -1

    isSolvable = True
    #gets the square with highest degree heuristic and checks for unsolvable squares
    for r in range(0, 9):
      for c in range(0, 9):
        if (numMoveArray[r][c] == 0 and currentBoard[r][c] == 0):#unsolvable
          isSolvable = False
        if (numMoveArray[r][c] > max):
          max = numMoveArray[r][c]
          maxRow = r
          maxCol = c

    if (max == 0):#solved (no more spaces to fill)
      return currentBoard

    if (not isSolvable):
      continue

    possVals = getPossibleValuesForSquare(currentBoard, maxRow, maxCol)
    if(possVals == 0):
      continue
    for i in range(0, len(possVals)):
      currentBoard[maxRow][maxCol] = possVals[i]
      #printPuzzle(currentBoard)
      stack.push(currentBoard)
      #print("push")

  print("Solution not found")
  return None



def solvePuzzleMinimum(sodukoArray):
  print("solvePuzzleMinimum")

  stack = Stack()
  stack.push(sodukoArray)
  while(not stack.isEmpty()):
    currentBoard = stack.pop().board
    #print("pop")

    #fill in any squares with 1 move
    numMoveArray = getNumValuesForEverySquare(currentBoard)
    changeMade = True
    while(changeMade):
      changeMade = False
      for r in range(0, len(currentBoard)):
        for c in range(0, len(currentBoard[r])):
          if (numMoveArray[r][c] == 1):
            changeMade = True
            #print(getPossibleValuesForSquare(currentBoard, r, c))
            currentBoard[r][c] = getPossibleValuesForSquare(currentBoard, r, c)[0]
            numMoveArray = getNumValuesForEverySquare(currentBoard)

    #checks if is solved
    #if(isSolved(currentBoard)):
    #  return currentBoard

    min = 11
    minRow = -1
    minCol = -1

    isSolvable = True
    #gets the square with lowest degree heuristic and checks for unsolvable squares
    for r in range(0, 9):
      for c in range(0, 9):
        if (numMoveArray[r][c] == 0 and currentBoard[r][c] == 0):#unsolvable
          isSolvable = False
        if (numMoveArray[r][c] < min and numMoveArray[r][c] > 0):
          min = numMoveArray[r][c]
          minRow = r
          minCol = c

    if (min == 11):#solved (no more spaces to fill)
      return currentBoard

    if (not isSolvable):
      continue

    possVals = getPossibleValuesForSquare(currentBoard, minRow, minCol)
    if(possVals == 0):
      continue
    for i in range(0, len(possVals)):
      currentBoard[minRow][minCol] = possVals[i]
      #printPuzzle(currentBoard)
      stack.push(currentBoard)
      #print("push")

  print("Solution not found")
  return None


#makes a solved puzzle
def makePuzzle():
  print("make puzzle")

  sodukoArray = [[0] * (9) for _ in range(9)]

  #soduko Array is represented by a 9 by 9 2-d array filled with ints
  #empty squares are set to 0

  #when a square with no possible moves is found, only changes a square that has the potential to solve the conflict
  #   (either same row, same column, or same square)

  while (not isSolved(sodukoArray)):#loops until solved

    for row in range(0, 9):
      for column in range(0, 9):#iterates through evey square

        if (sodukoArray[row][column] != 0):#square already has a value
          continue

        possVals = getPossibleValuesForSquare(sodukoArray, row, column)
        while(possVals == []):#square has no values it can be without violating a constraint

          #changes other possibly conflicting squares until a value can be given to the current square 
          changeValueInRowOrColumnOrSquare(sodukoArray, row, column)
          possVals = getPossibleValuesForSquare(sodukoArray, row, column)

        #sets the square to a random valid possible value that does not violate any constraints  
        sodukoArray[row][column] = possVals[randint(0, len(possVals) - 1)]



  #Guess and check (takes ~8 minutes)
  #while (not isSolved(sodukoArray)):
  #  randRow = randint(0, 8)
  #  randColumn = randint(0, 8)
  #  while True:
  #    possVals = getPossibleValuesForSquare(sodukoArray, randRow, randColumn)
  #    if(sodukoArray[randRow][randColumn] != 0):
  #      break
  #    if (possVals == []):
  #      sodukoArray[randint(0, 8)][randint(0, 8)] = 0
  #      continue
  #    sodukoArray[randRow][randColumn] = possVals[randint(0, len(possVals) - 1)]
  #    break


  return sodukoArray

#sets squares of a solved puzzle to zero until only a certain number of squares remain solved
def unsolvePuzzle(sodukoArray, startNumOfSquares):
  squaresLeftToUnsolve = len(sodukoArray) * len(sodukoArray[0]) - startNumOfSquares
  while (squaresLeftToUnsolve > 0):
    randRow = randint(0, len(sodukoArray) - 1)
    randColumn = randint(0, len(sodukoArray[0]) - 1)
    if (sodukoArray[randRow][randColumn] == 0):
      continue
    else:
      sodukoArray[randRow][randColumn] = 0
      squaresLeftToUnsolve -= 1
  
  return sodukoArray

#changes a value of a squares row, column, or square at random to a 0
def changeValueInRowOrColumnOrSquare(sodukoArray, row, column):
  randomInt = randint(1,3)
  if(randomInt == 1):#change row
    sodukoArray[randint(0, len(sodukoArray) - 1)][column] = 0
  elif(randomInt == 2):#change column
    sodukoArray[row][randint(0, len(sodukoArray[row]) - 1)] = 0
  else:#change square
    sodukoArray[randint((int(row / 3) * 3) - 1, (int(row / 3) * 3) + 3 - 1)][randint((int(column / 3) * 3 - 1), (int(column / 3) * 3) + 3 - 1)] = 0

#returns a matrix of every square with how many moves they can do
def getNumValuesForEverySquare(sodukoArray):
  
  numArray = [[0] * (9) for _ in range(9)]
  for r in range(9):
    for c in range(9):
      numArray[r][c] = len(getPossibleValuesForSquare(sodukoArray, r, c))

  return numArray

#returns true if soduko puzzle has all squares filled in with no conflicts
def isSolved(sodukoArray):
  for row in range(0, 9):
    for col in range(0, 9):
      squareVal = sodukoArray[row][col]

      if (squareVal == 0):#there is a square that is not filled in
        return False

      for r in range(len(sodukoArray)):#checks the row ignoring current square
        if (sodukoArray[r][col] == squareVal and r != row):
          return False

      for c in range(len(sodukoArray[0])):#checks the column ignoring current square
        if (sodukoArray[row][c] == squareVal and c != col):
          return False

      for r in range((int(row / 3) * 3), (int(row / 3) * 3) + 3):#checks the square
        for c in range((int(col / 3) * 3), (int(col / 3) * 3) + 3):
          if (sodukoArray[row][c] == squareVal and c != col and r != row):
            return False

  return True

#returns a list of all of the possible values a given square in the puzzle can be
def getPossibleValuesForSquare(sodukoArray, row, column):
  if(sodukoArray[row][column] != 0):
    return []

  possibleValues = [1,2,3,4,5,6,7,8,9]

  for r in range(len(sodukoArray)):#checks the row
    if (sodukoArray[r][column] in possibleValues):
      possibleValues.remove(sodukoArray[r][column])

  for c in range(len(sodukoArray[0])):#checks the column
    if (sodukoArray[row][c] in possibleValues):
      possibleValues.remove(sodukoArray[row][c])

  for r in range((int(row / 3) * 3), (int(row / 3) * 3) + 3):#checks the square
    for c in range((int(column / 3) * 3), (int(column / 3) * 3) + 3):
      if (sodukoArray[r][c] in possibleValues):
        possibleValues.remove(sodukoArray[r][c])

  return possibleValues

#prints the ascii representation of a soduko puzzle
def printPuzzle(sodukoArray):
  if(sodukoArray == None):
    print("Puzzle is null")
    return

  for r in range(len(sodukoArray)):
    for c in range(len(sodukoArray[r])):
      if (c == 3 or c == 6):
        print("|", end=" ")
      print(sodukoArray[r][c], end=" ")
    print("")
    if (r == 2 or r == 5):
      print("---------------------")

if __name__== "__main__":
  print("Main")
  startTime = datetime.datetime.now()
  puzzle = makePuzzle()
  endTime = datetime.datetime.now()
  print("time to make a puzzle: " + str(endTime - startTime))

  numPuzzle = getNumValuesForEverySquare(puzzle)

  #solvedPuzzle = [[8,2,7,1,5,4,3,9,6],[9,6,5,3,2,7,1,4,8],[3,4,1,6,8,9,7,5,2],[5,9,3,4,6,8,2,7,1],[4,7,2,5,1,3,6,8,9],[6,1,8,9,7,2,4,3,5],[7,8,6,2,3,5,9,1,4],[1,5,4,7,9,6,8,2,3],[2,3,9,8,4,1,5,6,7]]
  #solvedPuzzle = [[1, 3, 6, 8, 7, 5, 2, 9, 0], [4, 5, 7, 6, 2, 9, 8, 3, 0], [9, 2, 8, 1, 4, 3, 5, 7, 0], [2, 8, 3, 4, 9, 7, 1, 5, 0], [6, 4, 9, 5, 3, 1, 7, 8, 0], [7, 1, 5, 2, 6, 8, 9, 4, 0], [5, 9, 2, 7, 8, 6, 4, 1, 0], [8, 7, 1, 9, 5, 4, 3, 6, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
  #print("testing testing")
  #print(isSolved(solvedPuzzle))

  print("Puzzle:")
  printPuzzle(puzzle)

  print("Unsolved Puzzle:")
  puzzle = unsolvePuzzle(puzzle, 20)
  printPuzzle(puzzle)

  print("Resolved Puzzle Degree:")
  startTime = datetime.datetime.now()
  for i in range(0,1):
    solvePuzzleDegree(puzzle)
  endTime = datetime.datetime.now()
  print("time to solve puzzle degree 1 times: " + str(endTime - startTime))

  
  print("Resolved Puzzle Degree:")
  startTime = datetime.datetime.now()
  for i in range(0,1):
    solvePuzzleMinimum(puzzle)
  endTime = datetime.datetime.now()
  print("time to solve puzzle minimum 1 times: " + str(endTime - startTime))
  #printPuzzle(puzzle)

  #print("Moves:")
  #printPuzzle(numPuzzle)

