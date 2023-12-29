import unittest
from .Player import Player
from .Board import Board
from .Pawn import Pawn
from .Bishop import Bishop

class BishopTests(unittest.TestCase):
    def setUp(self):
        # Set up a board with bishops and other pieces
        self.chessboard = Board(Player('White', 'white'), Player('Black', 'black'))
        self.chessboard.addPiece(Bishop(self.chessboard.players[0], "c1"))  # White bishop
        self.chessboard.addPiece(Bishop(self.chessboard.players[1], "f8"))  # Black bishop
        # Adding pawns to test bishop's movement and capture
        self.chessboard.addPiece(Pawn(self.chessboard.players[1], "d2"))  # Black pawn
        self.chessboard.addPiece(Pawn(self.chessboard.players[0], "e5"))  # White pawn
        self.chessboard.currentTurn = self.chessboard.players[0]  # White starts

    def test_bishop_valid_move(self):
        # Test a valid move for the white bishop
        self.assertTrue(self.chessboard.play('c1', 'a3'))  # Move to h6

        # Test a valid move for the black bishop
        self.assertTrue(self.chessboard.play('f8', 'a3'))  # Move to a3

    def test_bishop_invalid_move(self):
        # Test an invalid move for the white bishop
        self.assertFalse(self.chessboard.play('c1', 'c3'))  # Bishops can't move straight
        self.chessboard.switchTurn()

        # Test an invalid move for the black bishop
        self.assertFalse(self.chessboard.play('f8', 'f7'))  # Bishops can't move straight

    def test_bishop_capture(self):
        # Test capturing a piece diagonally
        self.assertTrue(self.chessboard.play('c1', 'd2'))  # Bishop captures pawn at d4

    def test_bishop_blocked_by_piece(self):
        # Test bishop blocked by own piece
        self.assertFalse(self.chessboard.play('c1', 'e3'))  # Blocked by pawn at d2

if __name__ == '__main__':
    unittest.main()
