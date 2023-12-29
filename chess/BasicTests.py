import unittest

from .Board import Board

class BasicTests(unittest.TestCase):
    
    def test1(self):
        self.chessboard = Board.load(
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
        self.chessboard.currentTurn = self.chessboard.players[0]
        self.assertTrue( self.chessboard.play("e2", "e4" ) )
        self.assertTrue( self.chessboard.play("e7", "e5" ) )
        self.assertTrue( self.chessboard.play("f1", "c4" ) )
        self.assertTrue( self.chessboard.play("f8", "c5" ) )
        self.assertTrue( self.chessboard.play("d1", "h5" ) )
        self.assertTrue( self.chessboard.play("g8", "f6" ) )
        self.assertTrue( self.chessboard.play("h5", "f7" ) )
    
    def test2(self):
        self.chessboard = Board.load(
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
        self.chessboard.currentTurn = self.chessboard.players[0]
        self.assertTrue( self.chessboard.play("e2", "e4" ) )
        self.assertTrue( self.chessboard.play("e7", "e5" ) )
        self.assertTrue( self.chessboard.play("f1", "c4" ) )
        self.assertTrue( self.chessboard.play("f8", "c5" ) )
        self.assertTrue( self.chessboard.play("g1", "f3" ) )
        self.assertTrue( self.chessboard.play("b8", "c6" ) )
        self.assertTrue( self.chessboard.play("b1", "c3" ) )
        self.assertTrue( self.chessboard.play("g8", "f6" ) )
        self.assertTrue( self.chessboard.play("d2", "d3" ) )
        self.assertTrue( self.chessboard.play("d7", "d6" ) )
        self.assertTrue( self.chessboard.play("c1", "g5" ) )
        self.assertTrue( self.chessboard.play("c8", "g4" ) )
        self.assertTrue( self.chessboard.play("d1", "d2" ) )
        self.assertTrue( self.chessboard.play("d8", "d7" ) )
        self.assertTrue( self.chessboard.play("e1", "g1" ) )
        self.assertTrue( self.chessboard.play("e8", "c8" ) )

    def test3(self):
        self.chessboard = Board.load(
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
        self.assertTrue( self.chessboard.play("e2", "e4" ) )
        self.assertTrue( self.chessboard.play("e7", "e5" ) )
        self.assertTrue( self.chessboard.play("f1", "c4" ) )
        self.assertTrue( self.chessboard.play("f8", "c5" ) )
        self.assertTrue( self.chessboard.play("g1", "f3" ) )
        self.assertTrue( self.chessboard.play("b8", "c6" ) )
        self.assertTrue( self.chessboard.play("b1", "c3" ) )
        self.assertTrue( self.chessboard.play("g8", "f6" ) )
        self.assertTrue( self.chessboard.play("d2", "d3" ) )
        self.assertTrue( self.chessboard.play("d7", "d6" ) )
        self.assertTrue( self.chessboard.play("c1", "g5" ) )
        self.assertTrue( self.chessboard.play("c8", "g4" ) )
        self.assertTrue( self.chessboard.play("d1", "d2" ) )
        self.assertTrue( self.chessboard.play("d8", "d7" ) )
        self.assertTrue( self.chessboard.play("e1", "c1" ) )
        self.assertTrue( self.chessboard.play("e8", "g8" ) )
    
    def test4(self):
        self.chessboard = Board.load(
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
        self.assertTrue( self.chessboard.play("e2", "e4" ) )
        self.assertTrue( self.chessboard.play("e7", "e5" ) )
        self.assertTrue( self.chessboard.play("f1", "c4" ) )
        self.assertTrue( self.chessboard.play("f8", "c5" ) )
        self.assertTrue( self.chessboard.play("g1", "f3" ) )
        self.assertTrue( self.chessboard.play("b8", "c6" ) )
        self.assertTrue( self.chessboard.play("b1", "c3" ) )
        self.assertTrue( self.chessboard.play("g8", "f6" ) )
        self.assertTrue( self.chessboard.play("d2", "d3" ) )
        self.assertTrue( self.chessboard.play("d7", "d6" ) )
        self.assertTrue( self.chessboard.play("c1", "g5" ) )
        self.assertTrue( self.chessboard.play("c8", "g4" ) )
        self.assertTrue( self.chessboard.play("d1", "d2" ) )
        self.assertTrue( self.chessboard.play("d8", "d7" ) )
        self.assertTrue( self.chessboard.play("f3", "h4" ) )
        self.assertTrue( self.chessboard.play("f6", "h5" ) )
        self.assertFalse( self.chessboard.play("e1", "c1" ) )
    
    def test5(self):
        self.chessboard = Board.load(
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
        self.assertTrue( self.chessboard.play( "e2", "e4" ) )
        self.assertTrue( self.chessboard.play( "e7", "e5" ) )
        self.assertTrue( self.chessboard.play( "f1", "c4" ) )
        self.assertTrue( self.chessboard.play( "f8", "c5" ) )
        self.assertTrue( self.chessboard.play( "g1", "f3" ) )
        self.assertTrue( self.chessboard.play( "b8", "c6" ) )
        self.assertTrue( self.chessboard.play( "b1", "c3" ) )
        self.assertTrue( self.chessboard.play( "g8", "f6" ) )
        self.assertTrue( self.chessboard.play( "d2", "d3" ) )
        self.assertTrue( self.chessboard.play( "d7", "d6" ) )
        self.assertTrue( self.chessboard.play( "c1", "g5" ) )
        self.assertTrue( self.chessboard.play( "c8", "g4" ) )
        self.assertTrue( self.chessboard.play( "d1", "d2" ) )
        self.assertTrue( self.chessboard.play( "d8", "d7" ) )
        self.assertTrue( self.chessboard.play( "f3", "h4" ) )
        self.assertTrue( self.chessboard.play( "c5", "f2" ) )
        self.assertFalse( self.chessboard.play( "e1", "c1" ) )
        self.assertFalse( self.chessboard.play( "e1", "g1" ) )
    
    def test6(self):
        self.chessboard = Board.load(
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
        self.assertTrue( self.chessboard.play("e2", "e4") )
        self.assertTrue( self.chessboard.play("e7", "e5") )
        self.assertTrue( self.chessboard.play("d2", "d4") )
        self.assertTrue( self.chessboard.play("e5", "d4") )
        self.assertTrue( self.chessboard.play("c2", "c4") )
        self.assertTrue( self.chessboard.play("d4", "c3") )

if __name__ == '__main__':
    unittest.main()
