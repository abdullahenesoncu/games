import unittest
from .Player import Player
from .Board import Board
from .Pawn import Pawn
from .Rook import Rook

class RookTests(unittest.TestCase):
    def setUp(self):
        # Set up a board with rooks and other pieces
        self.chessboard = Board(Player('White', 'white'), Player('Black', 'black'))
        self.chessboard.addPiece(Rook(self.chessboard.players[0], "a1"))  # White rook
        self.chessboard.addPiece(Rook(self.chessboard.players[1], "h8"))  # Black rook
        # Adding pawns to test rook's movement and capture
        self.chessboard.addPiece(Pawn(self.chessboard.players[0], "a5"))  # White pawn
        self.chessboard.addPiece(Pawn(self.chessboard.players[1], "h2"))  # Black pawn
        self.chessboard.currentTurn = self.chessboard.players[0]  # White starts

    def test_rook_valid_move(self):
        # Test a valid move for the white rook
        self.assertTrue(self.chessboard.play('a1', 'a4'))  # Move to a4

        # Test a valid move for the black rook
        self.assertTrue(self.chessboard.play('h8', 'h5'))  # Move to h5

    def test_rook_invalid_move(self):
        # Test an invalid diagonal move for the white rook
        self.assertFalse(self.chessboard.play('a1', 'b2'))  # Rooks can't move diagonally
        self.chessboard.switchTurn()

        # Test an invalid diagonal move for the black rook
        self.assertFalse(self.chessboard.play('h8', 'g7'))  # Rooks can't move diagonally

    def test_rook_capture(self):
        # Test capturing a piece
        self.assertTrue(self.chessboard.play('a1', 'a3'))  # Rook captures pawn at a3

    def test_rook_blocked_by_piece(self):
        # Test rook blocked by own piece
        self.chessboard.addPiece(Pawn(self.chessboard.players[0], 'a2'))
        self.assertFalse(self.chessboard.play('a1', 'a4'))  # Blocked by pawn at a2

if __name__ == '__main__':
    unittest.main()
