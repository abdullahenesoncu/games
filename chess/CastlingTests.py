import unittest
from .Player import Player
from .Board import Board
from .Pawn import Pawn
from .Rook import Rook
from .Knight import Knight
from .Bishop import Bishop
from .Queen import Queen
from .King import King

class CastlingTests(unittest.TestCase):
    def setUp(self):
        # This setup creates a board with only kings and rooks for simplicity
        self.chessboard = Board(Player('White', 'white'), Player('Black', 'black'))
        self.chessboard.addPiece(King(self.chessboard.players[0], "e1"))  # White king
        self.chessboard.addPiece(Rook(self.chessboard.players[0], "a1")) # White queenside rook
        self.chessboard.addPiece(Rook(self.chessboard.players[0], "h1")) # White kingside rook
        self.chessboard.addPiece(King(self.chessboard.players[1], "e8")) # Black king
        self.chessboard.addPiece(Rook(self.chessboard.players[1], "a8")) # Black queenside rook
        self.chessboard.addPiece(Rook(self.chessboard.players[1], "h8")) # Black kingside rook
        self.chessboard.currentTurn = self.chessboard.players[0]  # White starts

    def test_kingside_castling_white(self):
        self.assertTrue(self.chessboard.play('e1', 'g1'))
    
    def test_kingside_castling_black(self):
        self.chessboard.switchTurn()
        self.assertTrue(self.chessboard.play('e8', 'g8'))

    def test_queenside_castling_white(self):
        self.assertTrue(self.chessboard.play('e1', 'c1'))

    def test_queenside_castling_black(self):
        self.chessboard.switchTurn()
        self.assertTrue(self.chessboard.play('e8', 'c8'))

    def test_castling_with_obstacle(self):
        bishop = Bishop(self.chessboard.players[0], "f1")
        self.chessboard.addPiece(bishop)
        self.assertFalse(self.chessboard.play('e1', 'g1'))

    def test_castling_while_in_check(self):
        # Put the white king in check
        self.chessboard.addPiece(Queen(self.chessboard.players[1], "e2"))
        self.assertFalse(self.chessboard.play('e1', 'g1'))  # Can't castle out of check

    def test_castling_through_check(self):
        # Place an opposing piece to attack a square the king passes through
        self.chessboard.addPiece(Queen(self.chessboard.players[1], "f3"))
        self.assertFalse(self.chessboard.play('e1', 'g1'))  # Can't castle through check

    def test_castling_after_king_moved(self):
        # Move the king and move it back
        self.chessboard.play('e1', 'f1')
        self.chessboard.play('f1', 'e1')
        self.assertFalse(self.chessboard.play('e1', 'g1'))  # Can't castle after the king has moved

if __name__ == '__main__':
    unittest.main()
