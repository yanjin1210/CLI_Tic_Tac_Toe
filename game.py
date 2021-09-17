"""
game class provide apis for other modules to make change to the game board
"""

from random import randrange
from time import sleep
from termcolor import colored

MOVES = ["X", "O"]

COLORS = {
    "X": "red",
    "O": "blue"
}

DASHED_LINE = "-------------"

END_MESSAGES = {
    "O": colored("O wins", "blue"),
    "X": colored("X wins", "red"),
    " ": colored("Draw", "yellow")
}


class Game:
    """
    define the game board handling game board rendering and game moves
    provide ai solvers for other modules to utilize
    """
    def __init__(self, is_with_ai = False, is_ai_turn = False):
        self.board = [[i * 3 + j + 1 for j in range(3)] for i in range(3)]
        self.cur_move = "X"
        self.next_move = "O"
        self.is_ended = False
        self.moves = []
        self.is_with_ai = is_with_ai
        self.is_ai_turn = is_ai_turn

    def is_cell_empty(self, row, col):
        """
        check if cell is empty
        :param row: row number
        :param col: column number
        :return: bool
        """
        return self.board[row][col] not in MOVES

    def make_move(self, row, col):
        """
        make a move in specific cell
        and make changes to other game status

        :param row: row number of cell
        :param col: column number of cell
        :return: None
        """
        if self.is_cell_empty(row, col):
            self.board[row][col] = self.cur_move
            self.cur_move, self.next_move = self.next_move, self.cur_move
            self.moves.append((row, col))
        else:
            print("Cell already occupied.")

    def clear_move(self, row, col):
        """
        clear the move at a specific cell
        and make changes to other game status

        :param row: row number of cell
        :param col: col number of cell
        :return: None
        """
        self.board[row][col] = row * 3 + col + 1
        self.cur_move, self.next_move = self.next_move, self.cur_move
        self.moves.pop()
        self.is_ended = False

    def print_row(self, row):
        """
        print a specific row in format
        :param row: row number
        :return: None
        """
        print("| ", end="")
        for j in range(3):
            move = self.board[row][j]
            print(colored(move, COLORS.get(move, "white")) + " | ", end="")
        print("")

    def print_board(self):
        """
        render the whole game board
        :return: None
        """
        print("")
        print(DASHED_LINE)
        for i in range(3):
            self.print_row(i)
            print(DASHED_LINE)
        print("")

    def is_row_winning(self, row) -> bool:
        """
        check if a row has the same move ("X" or "O")
        :param row: row number
        :return: bool
        True: the row is of the same move
        False: the row is not of the same move
        """
        for j in range(3):
            if self.board[row][j] != self.next_move:
                return False
        return True

    def is_col_winning(self, col):
        """
        check if a column has the same move ("X" or "O")
        :param col: column number
        :return: bool
        True: the column is of the same move
        False: the column is not of the same move
        """
        for i in range(3):
            if self.board[i][col] != self.next_move:
                return False
        return True

    def is_left_diag_winning(self):
        """
        check if a left diagonal has the same move ("X" or "O")
        :return: bool
        True: the left diagonal is of the same move
        False: the left diagonal is not of the same move
        """
        for i in range(3):
            if self.board[i][i] != self.next_move:
                return False
        return True

    def is_right_diag_winning(self):
        """
        check if a right diagonal has the same move ("X" or "O")
        :return: bool
        True: the right diagonal is of the same move
        False: the right diagonal is not of the same move
        """
        for i in range(3):
            if self.board[i][2-i] != self.next_move:
                return False
        return True

    def is_diag_winning(self, row, col):
        """
        check if the diagonals with the cell have the same move
        :param row: row number of the cell
        :param col: column number of the cell
        :return: bool
        True: at least one diagonal is of the same move
        False: the cell does not belong the a diagonal or diagonals is not of the same move
        """
        result = False
        if row == col:
            result |= self.is_left_diag_winning()
        if row + col == 2:
            result |= self.is_right_diag_winning()
        return result

    def get_result(self, row, col):
        """
        check and update game status after a move

        :param row: row number of the cell
        :param col: column number of the cell
        :return:
        str: game end message
        None: game is still going on
        """
        if self.is_row_winning(row) or self.is_col_winning(col) or self.is_diag_winning(row, col):
            self.is_ended = True
            return END_MESSAGES[self.next_move]
        if len(self.moves) == 9:
            self.is_ended = True
            return END_MESSAGES[" "]
        return None

    def get_candidates(self) -> [(int, int)]:
        """
        get the empty cells
        :return: [(row, col)]
        """
        candidates = []
        for i in range(3):
            for j in range(3):
                if self.is_cell_empty(i, j):
                    candidates.append((i, j))
        return candidates

    def is_winning_move(self, row, col) -> bool:
        """
        check if making the move will win or draw the game
        :param row: row number of cell
        :param col: column number of cell
        :return: bool
        True: this is a winning or drawing move
        False: this is not
        """
        self.make_move(row, col)
        res = self.get_result(row, col)
        self.clear_move(row, col)
        return bool(res)

    def is_losing_move(self, row, col) -> bool:
        """
        check if this is the winning move for your opponent
        :param row: row number of cell
        :param col: column number of cell
        :return: bool
        """
        self.cur_move, self.next_move = self.next_move, self.cur_move
        res = self.is_winning_move(row, col)
        self.cur_move, self.next_move = self.next_move, self.cur_move
        return res

    def solver_easy(self, candidates) -> (int, int):
        """
        simple ai solver will return a random move
        :param candidates: empty cells
        :return: row, col
        """
        return candidates[randrange(len(candidates))]

    def solver_mid(self, candidates) -> (int, int):
        """
        medium ai solver will check
        if there is a immediate winning or losing move and return the move
        if not return random move
        :param candidates: empty cells
        :return: row, col
        """
        winning_moves = []
        losing_moves = []
        neutral_moves = []

        for row, col in candidates:
            if self.is_winning_move(row, col):
                winning_moves.append((row, col))
            elif self.is_losing_move(row, col):
                losing_moves.append((row, col))
            else:
                neutral_moves.append((row, col))

        if winning_moves:
            return self.solver_easy(winning_moves)
        if losing_moves:
            return self.solver_easy(losing_moves)
        return self.solver_easy(neutral_moves)

    def solver_hard(self, candidates):
        """
        unbeatable ai solver utilize minmax algorithm to get the best move.
        :param candidates: empty cells
        :return: row, col
        """
        if len(self.moves) == 0:
            return self.solver_easy(candidates)
        if len(self.moves) == 8:
            return candidates[0]
        return self.use_min_max(candidates)

    def min_max(self, row, col) -> int:
        """
        minmax algorithm to evaluate a certain move
        :param row: row number
        :param col: column number
        :return: score
        1: this move could win the game
        0: this move could at least draw the game
        -1: this move could lose the game
        """
        score = 1
        self.make_move(row, col)
        res = self.get_result(row, col)
        if res == "Draw":
            score = 0
        elif res:
            score = 1
        else:
            for r, c in self.get_candidates():
                score = min(score, - self.min_max(r, c))
        self.clear_move(row, col)
        return score

    def use_min_max(self, candidates) -> (int, int):
        """
        choose the cells in candidates that will score the highest
        :param candidates: empty cells
        :return: row, col
        """
        score = -1
        result_row, result_col = candidates[0]
        for row, col in candidates:
            s = self.min_max(row, col)
            if s == 1:
                return row, col
            if s > score:
                result_row, result_col = row, col
                score = s
        return result_row, result_col

    def solver(self, diff):
        """
        display AI thinking message and return the move AI makes based on the difficulty
        :param diff: difficulty
        :return: row, col
        """
        print("AI is making a move...")
        sleep(2)
        candidates = self.get_candidates()
        if diff == 1:
            return self.solver_easy(candidates)
        if diff == 2:
            return self.solver_mid(candidates)
        if diff == 3:
            return self.solver_hard(candidates)

    def update_ai_turn(self):
        """
        After a successful move change player
        :return: None
        """
        self.is_ai_turn ^= True
