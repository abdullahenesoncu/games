from .Player import Player
from .GameBase import GameBase
from .Board import Board
from .helpers import XY2POS, POS2XY

class Qirkat( GameBase ):
    @classmethod
    def getInitialRepr( cls ):
        return 'ccccc/ccccc/cc1CC/CCCCC/CCCCC w -'
    
    @classmethod
    def getPossibleMoves( cls, repr ):
        board = Board.boardFromFEN( repr )
        res = []
        for x1 in range( board.columns ):
            for y1 in range( board.rows ):
                piece = board.getCell( x1, y1 )
                if piece is None:
                    continue
                if board.pieceToPlay and board.pieceToPlay != piece:
                    continue
                for dx, dy in piece.getPossibleDirections():
                    if board.canMove(piece, x1+dx, y1+dy):
                        if not board.move(piece, x1+dx, y1+dy):
                            assert(False)
                        res.append( (board.boardToFEN(), f'{XY2POS(x1,y1)}{XY2POS(x1+dx,y1+dy)}') )
                        board = Board.boardFromFEN( repr )
                        piece = board.getCell( x1, y1 )
                for (cx, cy), (gx, gy) in piece.getPossibleCaptures():
                    if board.canMove(piece, x1+gx, y1+gy):
                        if not board.move(piece, x1+gx, y1+gy):
                            assert(False)
                        res.append( (board.boardToFEN(), f'{XY2POS(x1,y1)}{XY2POS(x1+gx,y1+gy)}') )
                        board = Board.boardFromFEN( repr )
                        piece = board.getCell( x1, y1 )
        return res
    
    @classmethod
    def getScore(cls, repr):
        board = Board.boardFromFEN(repr)
        score = 0

        for x in range(5):
            for y in range(5):
                piece = board.getCell(x, y)
                if piece is not None:
                    if piece.player.color == 'white':
                        score += 1
                    else:
                        score -= 1

        return score
    
    @classmethod
    def isGameOver( cls, repr ):
        board = Board.boardFromFEN( repr )
        return board.isGameOver()
    
    @classmethod
    def winner( cls, repr ):
        board = Board.boardFromFEN( repr )
        assert( board.isGameOver() )
        if board.isDraw():
            return 0
        if board.currentTurn.color == 'white':
            return -1
        else:
            return 1
    
    def __init__( self, player1, player2 ):
        self.player1 = Player(player1, 'white')
        self.player2 = Player(player2, 'black')
        self.board = Board( player1, player2 ).boardFromFEN( self.getInitialRepr() )
    
    def parseInput( self, moveInput ):
        if 4 <= len(moveInput) <= 5:
            return moveInput[ :2 ], moveInput[ 2:4 ], moveInput[ 4: ]
        else:
            return None
    
    def getInput(self):
        moveInput = None
        while moveInput is None:
            moveInput = self.parseInput( input( 'Please Enter Your Move: ' ) )
        return moveInput
    
    def parseInput( self, moveInput ):
        if len(moveInput) == 4:
            return moveInput[ :2 ], moveInput[ 2:4 ]
        else:
            return None
    
    def getInput(self):
        moveInput = None
        while moveInput is None:
            moveInput = self.parseInput( input( 'Please Enter Your Move: ' ) )
        return moveInput

    def play( self, input ):
        print(input)
        input = self.parseInput(input)
        status = self.board.play(*input)
        assert( status )
    
    def run(self):
        while not self.chessboard.isGameOver():
            print( self.chessboard.boardToString() )
            moveInput = self.getInput()
            status = self.chessboard.play(*moveInput)
            if status == True:
                print("Move successful.")
            else:
                print("Invalid move. Try again.")
        if self.chessboard.isDraw():
            print( 'Draw!' )
        elif self.chessboard.isCheckmate(self.player1):
            print( f'{self.player2.name} win!' )
        else:
            print( f'{self.player1.name} win!' )

if __name__ == '__main__':
    Checker('Alice', 'Bob').run()
