import unittest

from .Game import Chess
from .Board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.chessboard = Board.boardFromFEN(Chess.getInitialRepr())

    def test_initial_board_setup(self):
        expected_board = (
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
        self.assertEqual(self.chessboard.boardToString(), expected_board)

    def test_load_board(self):
        board_string = (
            "  a b c d e f g h\n"
            "8 r . . . . . . r\n"
            "7 p p p p p p p p\n"
            "6 . . . . . . . .\n"
            "5 . . . . . . . .\n"
            "4 . . . . . . . .\n"
            "3 . . . . . . . .\n"
            "2 P P P P P P P P\n"
            "1 R . . . . . . R"
        )
        chessboard = Board.load( board_string )
        self.assertEqual(chessboard.boardToString(), board_string)

if __name__ == '__main__':
    unittest.main()
