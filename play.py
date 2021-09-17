""" This module will interact with player
    display the game board
    and let the player to play tic-tac-toe"""

from termcolor import colored

from game import Game


def get_ai() -> bool:
    """ check if player wants to play with ai:
        True: play with AI
        False: play with human
    """
    option = input("Do you want to play with AI?\n[Yes: Y]/[No: N]: ").strip().lower()
    if option in ["y", "n"]:
        return option == "y"
    print("Invalid input. Please enter \"Y\" or \"N\".")
    return get_ai()


def get_ai_turn() -> bool:
    """ check if AI will play the first turn
        True: AI first
        False: play first
    """
    turn = input("Do you want to play first?\n[Yes: Y]/[No: N]: ").strip().lower()
    if turn in ["y", "n"]:
        return turn == "n"
    print("Invalid input. Please enter \"Y\" or \"N\".")
    return get_ai_turn()


def get_difficulty() -> int:
    """ get the difficulty of AI the player wants to play with:
        1: easy
        2: medium
        3: hard
    """
    diff = input("Chose the difficulty of AI:\n1. Easy\n2. Medium\n3. Hard\n[1-3]: ").strip()
    if diff in ["1", "2", "3"]:
        return int(diff)
    print("Invalid input. Please choose from 1 to 3.")
    return get_difficulty()


def get_player_move() -> (int, int):
    """
    get the position of cell the player wants to play a move
    :return: row of cell, column of cell
    0 <= row, col <= 2
    """
    move = input("Please make your move [1-9]: ").strip()
    if move in [str(i) for i in range(1, 10)]:
        return divmod(int(move) - 1, 3)
    print("Invalid input.")
    return get_player_move()


def is_continue_playing() -> bool:
    """
    Check if player wants to play a new game after one game ends
    :return:
    True: player wants to play a new game
    False: player wants to quit
    """
    to_con = input("\nDo you want to play another game?\n[Yes: Y]/[No: N]: ").strip().lower()
    if to_con in ["y", "n"]:
        return to_con == "y"
    print("Invalid input. Please enter \"Y\" or \"N\".")
    return is_continue_playing()


def update_move(game, row, col):
    """
    make the move and print updated game board and
    :param game:
    :param row:
    :param col:
    :return: game result:
    None: game is still going
    str: game result message
    """
    game.make_move(row, col)
    game.print_board()
    return game.get_result(row, col)


def play_with_ai(diff, is_ai_turn):
    """
    start a new game and let player play with AI
    when game ended print the result
    :param diff: difficulty of AI
    :param is_ai_turn: is AI playing first turn
    :return: None
    """
    game = Game(True, is_ai_turn)
    game.print_board()
    while not game.is_ended:
        row, col = game.solver(diff) if game.is_ai_turn else get_player_move()
        if game.is_cell_empty(row, col):
            res = update_move(game, row, col)
            game.update_ai_turn()
        else:
            game.make_move(row, col)
    print(res)


def play_with_human():
    """
    start a new game and let player play with another player
    print result when game ended
    :return: None
    """
    game = Game()
    game.print_board()
    while not game.is_ended:
        row, col = get_player_move()
        res = update_move(game, row, col)
    print(res)


if __name__ == '__main__':
    print(colored("\nWelcome to Tic-Tac-Toe\n", "red"))
    to_continue = True
    while to_continue:
        withAI = get_ai()
        if withAI:
            play_with_ai(get_difficulty(), get_ai_turn())
        else:
            play_with_human()
        to_continue = is_continue_playing()
    print("\nThank you for playing. Bye!")
