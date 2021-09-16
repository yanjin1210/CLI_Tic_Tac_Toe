from termcolor import colored

from game import Game


def getAI():
    option = input("Do you want to play with AI?\n[Yes: Y]/[No: N]: ").strip().lower()
    if option in ["y", "n"]:
        return option == "y"
    print("Invalid input. Please enter \"Y\" or \"N\".")
    return getAI()


def getAITurn():
    turn = input("Do you want to play first?\n[Yes: Y]/[No: N]: ").strip().lower()
    if turn in ["y", "n"]:
        return turn == "n"
    print("Invalid input. Please enter \"Y\" or \"N\".")
    return getAITurn()


def getDifficulty():
    diff = input("Chose the difficulty of AI:\n1. Easy\n2. Medium\n3. Hard\n[1-3]: ").strip()
    if diff in ["1", "2", "3"]:
        return int(diff)
    print("Invalid input. Please choose from 1 to 3.")
    return getDifficulty()


def getMove():
    move = input("Please make your move [1-9]: ").strip()
    if move in [str(i) for i in range(1, 10)]:
        return divmod(int(move) - 1, 3)
    print("Invalid input.")
    return getMove()


def toContinue():
    toCon = input("\nDo you want to play another game?\n[Yes: Y]/[No: N]: ").strip().lower()
    if toCon in ["y", "n"]:
        return toCon == "y"
    print("Invalid input. Please enter \"Y\" or \"N\".")
    return toContinue()


def updateMove(game, row, col):
    game.makeMove(row, col)
    game.printBoard()
    return game.getResult(row, col)


def playWithAI(diff, isAITurn):
    game = Game()
    game.printBoard()
    while not game.isEnded:
        row, col = game.solver(diff) if isAITurn else getMove()
        isAITurn ^= True
        res = updateMove(game, row, col)
    print(res)


def playWithHuman():
    game = Game()
    game.printBoard()
    while not game.isEnded:
        row, col = getMove()
        res = updateMove(game, row, col)
    print(res)


if __name__ == '__main__':
    print(colored("\nWelcome to Tic-Tac-Toe\n", "red"))
    toCon = True
    while toCon:
        withAI = getAI()
        if withAI:
            playWithAI(getDifficulty(), getAITurn())
        else:
            playWithHuman()
        toCon = toContinue()
    print("\nThank you for playing. Bye!")