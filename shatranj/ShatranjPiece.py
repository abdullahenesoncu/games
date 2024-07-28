from .helpers import XY2POS, POS2XY
import math

class ShatranjPiece:
    def __init__(self, player, pos):
        self.x, self.y = POS2XY( pos )
        self.player = player
        self.possibleRegularMoves = None
        self.possibleCaptureMoves = None
        self.canJumpOverOthers = None
        self.multipleMove = None
        self.moved = False

    def canMove(self, x: int, y: int, board, ctrlCheck=True):
        if x == self.x and y == self.y:
            return False
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        if board.getCell( x, y ):
            return False
        diff = (x - self.x, y - self.y)
        if not self.multipleMove:
            if diff not in self.possibleRegularMoves:
                return False
        else:
            gcd = math.gcd( diff[ 0 ], diff[ 1 ] )
            diff = ( diff[ 0 ] / gcd, diff[ 1 ] / gcd )
            if diff not in self.possibleRegularMoves:
                return False
        piece = board.getCell(x, y)
        if piece and piece.player == self.player:
            return False
        if ctrlCheck and board.wouldBeInCheck( self, x, y ):
            return False
        return self.canJumpOverOthers or board.isPathClear(self.x, self.y, x, y)
    
    def canThreat(self, x: int, y: int, board, ctrlCheck=True):
        if x == self.x and y == self.y:
            return False
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        diff = (x - self.x, y - self.y)
        if not self.multipleMove:
            if diff not in self.possibleCaptureMoves:
                return False
        else:
            gcd = math.gcd( diff[ 0 ], diff[ 1 ] )
            diff = ( diff[ 0 ] / gcd, diff[ 1 ] / gcd )
            if diff not in self.possibleCaptureMoves:
                return False
        if ctrlCheck and board.wouldBeInCheck( self, x, y ):
            return False
        return self.canJumpOverOthers or board.isPathClear(self.x, self.y, x, y)

    def canCapture(self, x: int, y: int, board, ctrlCheck=True):
        if not self.canThreat(x, y, board, ctrlCheck=ctrlCheck):
            return False
        piece = board.getCell(x, y)
        if not piece or piece.player == self.player:
            return False
        return self.canJumpOverOthers or board.isPathClear(self.x, self.y, x, y)
    
    def move( self, x, y ):
        self.x = x
        self.y = y
        self.moved = True

    def __str__( self ):
        return f'{"W" if self.player.color=="white" else "B"}{self.name}({XY2POS(self.x, self.y)})'
