import unittest
from .Player import Player
from .Board import Board
from .Pawn import Pawn
from .Rook import Rook
from .Knight import Knight
from .Bishop import Bishop
from .Queen import Queen

class PawnPromotionTests(unittest.TestCase):
    def setUp(self):
        # Initialize a board with a pawn ready for promotion
        self.chessboard = Board(Player('White', 'white'), Player('Black', 'black'))
        self.chessboard.addPiece(Pawn(self.chessboard.players[0], "e7"))  # White pawn ready for promotion
        self.chessboard.currentTurn = self.chessboard.players[0]  # White starts

    def test_promote_to_queen(self):
        self.chessboard.play('e7', 'e8', 'q')
        promoted_piece = self.chessboard.getCell(4, 7)  # e8 position
        self.assertIsInstance(promoted_piece, Queen)

    def test_promote_to_rook(self):
        self.chessboard.play('e7', 'e8', 'r')
        promoted_piece = self.chessboard.getCell(4, 7)  # e8 position
        self.assertIsInstance(promoted_piece, Rook)

    def test_promote_to_bishop(self):
        self.chessboard.play('e7', 'e8', 'b')
        promoted_piece = self.chessboard.getCell(4, 7)  # e8 position
        self.assertIsInstance(promoted_piece, Bishop)

    def test_promote_to_knight(self):
        self.chessboard.play('e7', 'e8', 'n')
        promoted_piece = self.chessboard.getCell(4, 7)  # e8 position
        self.assertIsInstance(promoted_piece, Knight)

    def test_invalid_promotion_input(self):
        self.chessboard.play('e7', 'e8', 'x')  # Invalid input
        promoted_piece = self.chessboard.getCell(4, 7)  # e8 position
        self.assertIsInstance(promoted_piece, Pawn)  # Promotion should not occur

if __name__ == '__main__':
    unittest.main()
