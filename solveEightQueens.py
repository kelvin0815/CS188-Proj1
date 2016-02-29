import random
import copy
from optparse import OptionParser

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        solutionCounter = 0
        lectureCase = [[]]
        if lectureExample:
            lectureCase = [
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", "q", ".", ".", ".", "."],
            ["q", ".", ".", ".", "q", ".", ".", "."],
            [".", "q", ".", ".", ".", "q", ".", "q"],
            [".", ".", "q", ".", ".", ".", "q", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ]
        for i in range(0,numberOfRuns):
            if self.search(Board(lectureCase), verbose).getNumberOfAttacks() == 0:
                solutionCounter+=1
        print "Solved:",solutionCounter,"/",numberOfRuns

    def search(self, board, verbose):
        newBoard = board
        i = 0
        while True:
            if verbose:
                print "iteration ",i
                print newBoard.toString()
                print newBoard.getCostBoard().toString()
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks) = newBoard.getBetterBoard()
            i+=1
            if currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [["." for i in range(0,8)] for j in range(0,8)]
        for i in range(0,8):
            tmpSquareArray[random.randint(0,7)][i] = "q"
        return tmpSquareArray

    def toString(self):
        s = ""
        for i in range(0,8):
            for j in range(0,8):
                s += str(self.squareArray[i][j]) + " "
            s += "\n"
        return s + "# attacks: "+str(self.getNumberOfAttacks())

    def getCostBoard(self):
        costBoard = copy.deepcopy(self)
        for r in range(0,8):
            for c in range(0,8):
                if self.squareArray[r][c] == "q":
                    for rr in range(0,8):
                        if rr!=r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = "."
                            testboard.squareArray[rr][c] = "q"
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        " *** MY CODE HERE *** "
        #Solution test
        currentNumberOfAttacks = self.getNumberOfAttacks()
        if currentNumberOfAttacks == 0:
            return (self, currentNumberOfAttacks)
        costBoard = self.getCostBoard()
        #Get the minimum number of attacks from costBoard and corresponding candidates
        minAttack = min([costBoard.squareArray[r][c] for r in range(0, 8) for c in range(0, 8)])
        candidates = [(r, c) for r in range(0, 8) for c in range(0, 8) if costBoard.squareArray[r][c] == minAttack]
        # Case 1: minAttack is less than or equal to currentNumberOfAttacks
        if minAttack <= currentNumberOfAttacks:
            #Random Selection from candidates
            newRow, newCol = random.choice(candidates)
            betterBoard = copy.deepcopy(self)
            oldRow = [r for r in range(0, 8) if costBoard.squareArray[r][newCol] == "q"][0]
            #Queen Moving
            betterBoard.squareArray[oldRow][newCol] = "."
            betterBoard.squareArray[newRow][newCol] = "q"
            return (betterBoard, betterBoard.getNumberOfAttacks())
        # Case 2: minAttack is greater than currentNumberOfAttacks (local minimum)
        else:
            return (self, currentNumberOfAttacks)

    def getNumberOfAttacks(self):
        " *** MY CODE HERE *** "
        attacks = 0
        directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)]
        for r in range(0, 8):
            for c in range(0, 8):
                #Loop over all Queens
                if self.squareArray[r][c] == "q":
                    for direction in directions:
                        dRow, dCol = direction
                        for k in range(1, 8):
                            nextRow, nextCol = r + k * dRow, c + k * dCol
                            #Check if next slot is out of board
                            if nextRow in range(0, 8) and nextCol in range(0, 8):
                                if self.squareArray[nextRow][nextCol] == "q":
                                    attacks += 1
        #Each attack is counted twice
        return attacks / 2

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    #random.seed(0)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
