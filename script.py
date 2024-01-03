from chess.Board import Board
from chess.Game import Chess
from chess.helpers import XY2POS, POS2XY

board = Board.boardFromFEN('r1b1Qk1r/p4ppp/3b1n2/8/8/8/1P1PPPPP/2B1KB1R b K - 4 12')
print(Chess.getPossibleMoves('r1b1Qk1r/p4ppp/3b1n2/8/8/8/1P1PPPPP/2B1KB1R b K - 4 12'))
print(board.isGameOver())