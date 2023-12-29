import unittest
from .Player import Player
from .Board import Board
from .Pawn import Pawn
from .Knight import Knight

class KnightTests(unittest.TestCase):
    def setUp(self):
        # Set up a board with knights and other pieces
        self.chessboard = Board(Player('White', 'white'), Player('Black', 'black'))
        self.chessboard.addPiece(Knight(self.chessboard.players[0], "b1"))
        self.chessboard.addPiece(Knight(self.chessboard.players[1], "g8"))
        # Adding other pieces to test knight's jumping ability
        self.chessboard.addPiece(Pawn(self.chessboard.players[0], "c2"))
        self.chessboard.addPiece(Pawn(self.chessboard.players[0], "a2"))
        self.chessboard.addPiece(Pawn(self.chessboard.players[1], "f7"))
        self.chessboard.addPiece(Pawn(self.chessboard.players[1], "h7"))
        self.chessboard.currentTurn = self.chessboard.players[0]

    def test_knight_valid_move(self):
        # Test a valid move for the white knight
        self.assertTrue(self.chessboard.play('b1', 'c3'))  # Move to c3
        
        # Test a valid move for the black knight
        self.assertTrue(self.chessboard.play('g8', 'h6'))  # Move to h6

    def test_knight_invalid_move(self):
        # Test an invalid move for the white knight
        self.assertFalse(self.chessboard.play('b1', 'b3'))  # Knights can't move straight
        self.chessboard.switchTurn()

        # Test an invalid move for the black knight
        self.assertFalse(self.chessboard.play('g8', 'g6'))  # Knights can't move straight

    def test_knight_capture(self):
        # Add a black pawn at c3
        self.chessboard.addPiece(Pawn(self.chessboard.players[1], 'c3'))
        self.assertTrue(self.chessboard.play('b1', 'c3'))  # Knight captures pawn at c3
    
    def test_knight_jump_over_pieces(self):
        # Test white knight jumping over own pawns
        self.assertTrue(self.chessboard.play('b1', 'c3'))  # Jump over pawn at a2 and c2

        # Test black knight jumping over own pawns
        self.assertTrue(self.chessboard.play('g8', 'h6'))  # Jump over pawn at f7 and h7

    def test_knight_invalid_move_over_pieces(self):
        # Test invalid move for a knight even with pieces in between
        self.assertFalse(self.chessboard.play('b1', 'b3'))  # Invalid move for knight
        self.chessboard.switchTurn()

        # Test invalid move for a knight even with pieces in between
        self.assertFalse(self.chessboard.play('g8', 'g6'))  # Invalid move for knight

if __name__ == '__main__':
    unittest.main()
