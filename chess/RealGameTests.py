import unittest

from .Game import Chess
from .Board import Board
from .Player import Player
import chess.pgn

class RealGameTests(unittest.TestCase):
    def setUp(self):
        self.chessboard = Board.loadFEN(Chess.getInitialRepr())

    def fileTest(self, filename):
        pgn = open( filename )
        while True:
            game = chess.pgn.read_game( pgn )
            if not game:
                break
            board = game.board()
            self.setUp()
            for move in game.mainline_moves():
                prev = self.chessboard.dump()
                r = self.chessboard.play( str(move)[:2], str(move)[2:4], str(move)[4:] or None )
                board.push( move )
                expectedBoard = ['  a b c d e f g h'] + str(board).split('\n')
                expectedBoard[1] = '8 ' + expectedBoard[1]
                expectedBoard[2] = '7 ' + expectedBoard[2]
                expectedBoard[3] = '6 ' + expectedBoard[3]
                expectedBoard[4] = '5 ' + expectedBoard[4]
                expectedBoard[5] = '4 ' + expectedBoard[5]
                expectedBoard[6] = '3 ' + expectedBoard[6]
                expectedBoard[7] = '2 ' + expectedBoard[7]
                expectedBoard[8] = '1 ' + expectedBoard[8]
                expectedBoard = '\n'.join(expectedBoard)
                if not r or expectedBoard != self.chessboard.dump():
                    print()
                    print("=====PREV=====")
                    print(prev)
                    print("=====Move=====")
                    print(move, r)
                    print("=====Found====")
                    print(self.chessboard.dump())
                    print(self.chessboard.dumpFEN())
                    print("====Expected==")
                    print(expectedBoard)
                    print(board.fen())
                self.assertEqual( expectedBoard, self.chessboard.dump() )
                self.assertTrue( r )
    
    def test_NajdorfTests(self):
        self.fileTest( "data/Najdorf.pgn" )
    
    def test_KasparovGary(self):
        self.fileTest( "data/KasparovGary.pgn" )

if __name__ == '__main__':
    unittest.main()
