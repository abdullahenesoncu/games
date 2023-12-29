import unittest

from .Board import Board
from .Player import Player
import chess
import json

class FENTests(unittest.TestCase):
    def setUp(self):
        self.player1 = Player('Alice', 'white')
        self.player2 = Player('Bob', 'black')

    def fileTest(self, filename):
        data = json.load( open( filename,'r' ) )
        for testcase in data[ 'testCases' ]:
            board = chess.Board( testcase[ 'start' ][ 'fen' ] )
            for trial in testcase[ 'expected' ]:
                chessboard = Board.loadFEN( testcase[ 'start' ][ 'fen' ] )
                move = str( board.parse_san( trial[ 'move' ] ) )
                fromPos = move[ :2 ]
                toPos = move[ 2:4 ]
                additionalInput = move[ 4: ]
                prev = chessboard.dump()
                r = chessboard.play( fromPos, toPos, additionalInput )
                if not r or chessboard.dumpFEN() != trial[ 'fen' ]:
                    print()
                    print("=====PREV=====")
                    print(prev)
                    print(testcase['start']['fen'])
                    print("=====Move=====")
                    print(move, r)
                    print("=====Found====")
                    print(chessboard.dumpFEN())
                    print("====Expected==")
                    print(trial['fen'])
                self.assertEqual( chessboard.dumpFEN(), trial[ 'fen' ] )
    
    def test_castling(self):
        self.fileTest( 'data/castling.json' )
    
    def test_pawns(self):
        self.fileTest( 'data/pawns.json' )
    
    def test_promotions(self):
        self.fileTest( 'data/promotions.json' )
    
    def test_standard(self):
        self.fileTest( 'data/standard.json' )
    
    def test_taxing(self):
        self.fileTest( 'data/taxing.json' )
    
    def test_famous(self):
        self.fileTest( 'data/famous.json' )

if __name__ == '__main__':
    unittest.main()