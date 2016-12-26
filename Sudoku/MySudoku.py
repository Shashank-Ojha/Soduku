from time import time
from math import *

"""
+--------------------------+
|                          |
|      Shashank Ojha       |
|        Period 1          |
|                          |
+--------------------------+
"""

tic = time();

file = "sudokuHard.txt"
TotalNum = 9
Twidth = 9  #Total -c
Tlength = 9 #-r
Bwidth = 3  #box x - c
Blength = 3 #box y - r

class slot:
    val = 0
    rowMatrix, colMatrix, boxMatrix, possible = [], [], [], []

    def __init__(self, val):
       self.val = val
       self.rowMatrix, self.colMatrix, self.boxMatrix= [], [], []
       if val == '.':
            self.possible = [str(x) for x in range(1,TotalNum+1)]

    def setValue(self, val):
       self.val = val
    def addRow(self, val):
       self.rowMatrix.append(val)
    def addCol(self, val):
       self.colMatrix.append(val)
    def addBox(self, val):
       self.boxMatrix.append(val)
    def changePossible(self, data):
       self.possible = data
    def removeFromPossible(self, val):
       if(val in self.possible):
            self.possible.remove(val)
    def emptyPossible(self):
        self.possible = []

def makePuzzles(file):
    file = open(file , 'r')
    puzzles = file.read().split()
    return puzzles

def printPuzzle(puzzle):
    for x in range(Twidth):
        for y in range(Tlength):
            print (puzzle[Twidth*x + y] + " "),;
        print
    print

def printMatrix(matrix):
    for x in range(Twidth):
        for y in range(Tlength):
            print matrix[(x,y)].val,
        print
    print

def buildNeighbors(matrix, slot, r, c):
    for x in range(Twidth):
        slot.addRow(matrix[(r,x)].val)
    for y in range(Tlength):
        slot.addCol(matrix[(y,c)].val)
    r,c  = int(r/Blength), int(c/Bwidth)
    for i in range(r*Blength, r*Blength+3):
        for j in range(c*Bwidth, c*Bwidth+3):
            slot.addBox(matrix[(i,j)].val)

def solve(matrix):
    for r in range(Tlength):
        for c in range(Twidth):
            if matrix[(r,c)].val == '.':
                tempPossible = list(matrix[(r,c)].possible)
                for val in tempPossible:
                    if val in matrix[(r,c)].rowMatrix or val in matrix[(r,c)].colMatrix or val in matrix[(r,c)].boxMatrix:
                        matrix[(r,c)].removeFromPossible(val)
                if len(matrix[(r,c)].possible) != 1:
                    onlyPossible = isOnlyPlace(matrix, r, c)
                    if onlyPossible != -1:
                         matrix[(r,c)].possible = [onlyPossible]
                if len(matrix[(r,c)].possible) == 1:
                    updateCell(matrix, r, c)
                    recursiveCheck(matrix, r, c)
    if(correct(matrix) == False):
        guess(matrix)

def guess(matrix):
    min = Tlength+Twidth  #bigger then possible
    location = -1;
    for r in range(Tlength):
        for c in range(Twidth):
            if 0 < len(matrix[(r,c)].possible) < min:
                location = (r,c)
                min = len(matrix[(r,c)].possible)
    if location == -1:
        return
    r,c = location

    copy = copyMatrix(matrix)
    copyOfPossible = list(matrix[location].possible)

    for value in copyOfPossible:
        matrix[location].setValue(value)
        updatePossible(matrix, value, r, c)
        matrix[location].emptyPossible()
        solve(matrix)
        if(correct(matrix)):
            return
        restoreValues(matrix, copy) #next Guess

def restoreValues(matrix, oldMatrix):
    for r in range(Tlength):
        for c in range(Twidth):
            matrix[(r,c)] = copySlot(oldMatrix[(r,c)])

def isOnlyPlace(matrix, r, c):
    for x in matrix[(r,c)].possible:
        inRow = False
        for i in range(Tlength):
            if i == r: continue
            if x in matrix[(i,c)].possible:
                inRow = True
                break
        if inRow == False: return x
        inCol = False
        for j in range(Twidth):
            if j == c: continue
            if x in matrix[(r,j)].possible:
                inCol = True
                break
        if inCol == False:return x
        inBox = False
        s, d = int(r/Blength), int(c/Bwidth)
        for a in range(s*Blength, s*Blength+3):
             for b in range(d*Bwidth, d*Bwidth+3):
                 if a == r and b == c: continue
                 if x in matrix[(a,b)].possible:
                     inBox = True
                     break
        if inBox == False: return x
    return -1

def copyMatrix(matrix):
    copy = {}
    for x in range(Tlength):
        for y in range(Twidth):
            copy[(x,y)] = copySlot(matrix[(x,y)])
    return copy

def copySlot(toCopy):
    copy = slot(toCopy.val)
    for a in toCopy.rowMatrix: copy.addRow(a)
    for b in toCopy.colMatrix: copy.addCol(b)
    for c in toCopy.boxMatrix: copy.addBox(c)
    tempPossible = list(toCopy.possible)
    copy.changePossible(tempPossible)
    return copy

def recursiveCheck(matrix, r, c):
    for x in range(Twidth):
        if len(matrix[(r,x)].possible) == 1:
            updateCell(matrix, r, x)
            recursiveCheck(matrix, r, x)
    for y in range(Tlength):
        if len(matrix[(y,c)].possible) == 1:
            updateCell(matrix, y, c,)
            recursiveCheck(matrix, y, c)
    r, c = int(r/Blength), int(c/Bwidth)
    for i in range(r*Blength, r*Blength+3):
        for j in range(c*Bwidth, c*Bwidth+3):
            if len(matrix[(i,j)].possible) == 1:
                updateCell(matrix, i, j,)
                recursiveCheck(matrix, i, j)

def updateCell(matrix, r, c,): #new value of matrix is the only possible value; updates the possible values of neighbors of that cell; clears the possible array
    matrix[(r,c)].setValue(matrix[(r,c)].possible[0])
    updatePossible(matrix, matrix[(r,c)].possible[0], r, c)
    matrix[(r,c)].emptyPossible()

def updatePossible(matrix, val, r,c):
    for x in range(Twidth):
        matrix[(r,x)].removeFromPossible(val)
    for y in range(Tlength):
        matrix[(y,c)].removeFromPossible(val)
    r, c = int(r/Blength), int(c/Bwidth)
    for i in range(r*Blength, r*Blength+3):
        for j in range(c*Bwidth, c*Bwidth+3):
            matrix[(i,j)].removeFromPossible(val)

def correct(matrix):
    for x in range(Tlength):
        #Check Rows
        all = [str(a) for a in range(1,TotalNum+1)]
        for i in range(Twidth):
            if matrix[(x,i)].val in all: all.remove(matrix[(x,i)].val)
        if len(all) > 0: return False
    for y in range(Twidth):
        #Check Cols
        all = [str(a) for a in range(1,TotalNum+1)]
        for i in range(Tlength):
            if matrix[(i,y)].val in all: all.remove(matrix[(i,y)].val)
        if len(all) > 0: return False

        #Check Boxes
    for x in range(Tlength):
        x = int(x/Blength)
        for y in range(Twidth):
            all = [str(a) for a in range(1,TotalNum+1)]
            y = int(y/Bwidth)
            for i in range(x*Blength, x*Blength+3):
                for j in range(y*Bwidth, y*Bwidth+3):
                    if matrix[(i,j)].val in all:
                        all.remove(matrix[(i,j)].val)
            if len(all) > 0: return False
    return True

def construct(puzzle, matrix, numPuzzles):
    numPuzzles += 1
    print "Given:"
    printPuzzle(puzzle)
    r,c = 0,0
    for cell in puzzle:
        matrix[(r,c)] = slot(cell)
        c+=1
        if c>= Twidth:
            c=0
            r+=1
    r,c= 0,0
    for cell in puzzle: #we have to this later because puzzle isn't complete before
        buildNeighbors(matrix, matrix[(r,c)], r, c)
        c+=1
        if c>= Twidth:
            c=0
            r+=1
    return matrix, numPuzzles

def run():
    puzzles = makePuzzles(file)
    matrix = {}
    numPuzzles, solved = 0, 0
    for puzzle in puzzles:
        matrix, numPuzzles = construct(puzzle, matrix, numPuzzles)
        solve(matrix)
        print "Solution:"
        printMatrix(matrix)
        if correct(matrix):
            print "This Matrix is Correct\n"
            solved +=1
        else: print "Incorrect\n"

    print "solved", solved, "of the", numPuzzles, "puzzles"
    print 'time:', time()-tic

#MAIN---------------------------------------------
run()

