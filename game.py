from random import randrange
from termcolor import colored
import time

MOVES = ["X", "O"]

COLORS = {
    "X": "red",
    "O": "blue"
}

DASHED_LINE = "-------------"

END_MESSAGES = {
    "O": colored("O", "blue") + " wins",
    "X": colored("X", "red") + " wins",
    " ": "Draw"
}


class Game:
    def __init__(self):
        self.board = [[i * 3 + j + 1 for j in range(3)] for i in range(3)]
        self.curMove = "X"
        self.nextMove = "O"
        self.isEnded = False
        self.moves = []

    def makeMove(self, row, col):
        if self.board[row][col] in MOVES:
            print("Cell already occupied.")
        else:
            self.board[row][col] = self.curMove
            self.curMove, self.nextMove = self.nextMove, self.curMove
            self.moves.append((row, col))

    def clearMove(self, row, col):
        self.board[row][col] = row * 3 + col + 1
        self.curMove, self.nextMove = self.nextMove, self.curMove
        self.moves.pop()
        self.isEnded = False

    def printRow(self, row):
        print("| ", end="")
        for j in range(3):
            move = self.board[row][j]
            print(colored(move, COLORS.get(move, "white")) + " | ", end="")
        print("")

    def printBoard(self):
        print("")
        print(DASHED_LINE)
        for i in range(3):
            self.printRow(i)
            print(DASHED_LINE + "\n")

    def checkRowWin(self, row):
        for j in range(3):
            if self.board[row][j] != self.nextMove:
                return False
        return True

    def checkColWin(self, col):
        for i in range(3):
            if self.board[i][col] != self.nextMove:
                return False
        return True

    def checkLeftDiagWin(self):
        for i in range(3):
            if self.board[i][i] != self.nextMove:
                return False
        return True

    def checkRightDiagWin(self):
        for i in range(3):
            if self.board[i][2-i] != self.nextMove:
                return False
        return True

    def checkDiagWin(self, row, col):
        result = False
        if row == col:
            result |= self.checkLeftDiagWin()
        if row + col == 2:
            result |= self.checkRightDiagWin()
        return result

    def getResult(self, row, col):
        if self.checkRowWin(row) or self.checkColWin(col) or self.checkDiagWin(row, col):
            self.isEnded = True
            return END_MESSAGES[self.nextMove]
        elif len(self.moves) == 9:
            self.isEnded = True
            return END_MESSAGES[" "]
        else:
            return None

    def getCandidates(self):
        candidates = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] not in MOVES:
                    candidates.append((i, j))
        return candidates

    def isWinningMove(self, row, col):
        self.makeMove(row, col)
        res = self.getResult(row, col)
        self.clearMove(row, col)
        return True if res else False

    def isLosingMove(self, row, col):
        self.curMove, self.nextMove = self.nextMove, self.curMove
        res = self.isWinningMove(row, col)
        self.curMove, self.nextMove = self.nextMove, self.curMove
        return res

    def solverEasy(self, candidates):
        return candidates[randrange(len(candidates))]

    def solverMid(self, candidates):
        winningMoves = []
        losingMoves = []
        neutralMoves = []
        for row, col in candidates:
            if self.isWinningMove(row, col):
                winningMoves.append((row, col))
            elif self.isLosingMove(row, col):
                losingMoves.append((row, col))
            else: neutralMoves.append((row, col))
        if len(winningMoves):
            return self.solverEasy(winningMoves)
        elif len(losingMoves):
            return self.solverEasy(losingMoves)
        else: return self.solverEasy(neutralMoves)

    def solverHard(self, candidates):
        if len(self.moves) == 0:
            return self.solverEasy(candidates)
        elif len(self.moves) == 8:
            return candidates[0]
        else:
            score = -1
            resultRow, resultCol = candidates[0]
            for row, col in candidates:
                s = self.minMax(row, col)
                if s == 1:
                    return row, col
                elif s > score:
                    resultRow, resultCol = row, col
                    score = s
            return resultRow, resultCol

    def minMax(self, row, col) -> int:
        score = 1
        self.makeMove(row, col)
        res = self.getResult(row, col)
        if res == "Draw": score = 0
        elif res: score = 1
        else:
            for r, c in self.getCandidates():
                score = min(score, -self.minMax(r, c))
        self.clearMove(row, col)
        return score

    def solver(self, diff):
        print("AI is making a move...")
        time.sleep(2)
        candidates = self.getCandidates()
        if diff == 1:
            return self.solverEasy(candidates)
        if diff == 2:
            return self.solverMid(candidates)
        if diff == 3:
            return self.solverHard(candidates)

