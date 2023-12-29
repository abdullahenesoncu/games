import unittest

from .Player import Player
from .Board import Board
from .Pawn import Pawn

class PawnTests(unittest.TestCase):
    def setUp(self):
        # Set up a board with pawns and other pieces
        self.chessboard = Board(Player('White', 'white'), Player('Black', 'black'))
        self.chessboard.addPiece(Pawn(self.chessboard.players[0], "a2"))  # White pawn
        self.chessboard.addPiece(Pawn(self.chessboard.players[0], "a5"))  # White pawn
        self.chessboard.addPiece(Pawn(self.chessboard.players[1], "h7"))  # Black pawn
        # Adding a piece for potential capture
        self.chessboard.addPiece(Pawn(self.chessboard.players[1], "b3"))  # Black pawn
        self.chessboard.addPiece(Pawn(self.chessboard.players[1], "b6"))  # Black pawn
        self.chessboard.currentTurn = self.chessboard.players[0]  # White starts

    def test1(self):
        chessboard = Board.load(
            "  a b c d e f g h\n"
            "8 r n b q k b n r\n"
            "7 p p p p p p p p\n"
            "6 . . . . . . . .\n"
            "5 . . . . . . . .\n"
            "4 . . . . . . . .\n"
            "3 . . . . . . . .\n"
            "2 P P P P P P P P\n"
            "1 R N B Q K B N R"
        )
        chessboard.currentTurn = chessboard.players[0]
        self.assertTrue( chessboard.play( 'a2', 'a3' ) )
        self.assertTrue( chessboard.play( 'a7', 'a5' ) )
        self.assertTrue( chessboard.play( 'b2', 'b4' ) )
        self.assertTrue( chessboard.play( 'a5', 'b4' ) )

    def test_pawn_single_move(self):
        # Test a single forward move
        self.assertTrue(self.chessboard.play('a2', 'a3'))  # Move one square forward
        self.assertTrue(self.chessboard.play('h7', 'h6'))  # Move one square forward

    def test_pawn_double_move(self):
        # Test the double move from starting position
        self.assertTrue(self.chessboard.play('a2', 'a4'))  # Move two squares forward from starting position
        self.assertTrue(self.chessboard.play('h7', 'h5'))  # Move two squares forward from starting position

    def test_pawn_capture(self):
        # Test capturing diagonally
        self.assertTrue(self.chessboard.play('a5', 'b6'))  # Capture diagonally
        self.assertTrue(self.chessboard.play('b3', 'a2'))  # Capture diagonally

    def test_pawn_invalid_move(self):
        # Test an invalid move (moving backwards or sideways)
        self.assertFalse(self.chessboard.play('a5', 'a4'))  # Pawns cannot move backwards
        self.chessboard.switchTurn()
        self.assertFalse(self.chessboard.play('h6', 'g6'))  # Pawns cannot move sideways

    def test_pawn_blocked(self):
        # Test pawn blocked by another piece
        self.chessboard.addPiece(Pawn(self.chessboard.players[0], 'a4'))
        self.assertFalse(self.chessboard.play('a3', 'a4'))  # Blocked by another pawn

if __name__ == '__main__':
    unittest.main()
