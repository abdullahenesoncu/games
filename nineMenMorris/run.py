from .Game import TicTacToe
from .Board import Board

if __name__ == '__main__':
    TicTacToe('Alice', 'Bob').run()
    #board = Board.loadFEN('x..o.... x')
    '''Board.load(
        "  1 2 3\n"
        "1 x o x\n"
        "2 . o .\n"
        "3 . . ."
    )'''
