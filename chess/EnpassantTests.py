import unittest
from .Player import Player
from .Board import Board
from .Pawn import Pawn

class EnpassantTests(unittest.TestCase):
    def setUp(self):
        # This setup creates a board with only the necessary pawns for en passant
        self.chessboard = Board(Player('White', 'white'), Player('Black', 'black'))
        self.chessboard.addPiece(Pawn(self.chessboard.players[0], "e2"))  # White pawn
        self.chessboard.addPiece(Pawn(self.chessboard.players[1], "d7"))  # Black pawn

    def test_en_passant_capture_white(self):
        # Move white pawn two steps forward
        self.assertTrue(self.chessboard.play('e2', 'e4'))
        # Move black pawn two steps forward beside white pawn
        self.assertTrue(self.chessboard.play('d7', 'd5'))
        # Perform en passant capture
        self.assertTrue(self.chessboard.play('e4', 'd5', 'true'))

    def test_en_passant_capture_black(self):
        # Similar setup for black performing en passant
        # Move black pawn two steps forward
        self.chessboard.switchTurn()
        self.assertTrue(self.chessboard.play('d7', 'd5'))
        # Move white pawn two steps forward beside black pawn
        self.assertTrue(self.chessboard.play('e2', 'e4'))
        # Perform en passant capture
        self.assertTrue(self.chessboard.play('d5', 'e4', 'true'))

if __name__ == '__main__':
    unittest.main()