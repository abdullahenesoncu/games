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
        if not self.canJumpOverOthers and not board.isPathClear(self.x, self.y, x, y):
            return False
        if ctrlCheck and board.wouldBeInCheck( self, x, y ):
            return False
        return True

    def canThreat(self, x: int, y: int, board, ctrlCheck=True):
        if x == self.x and y == self.y:
            return False
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        piece = board.getCell(x, y)
        if piece and piece.player == self.player:
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
        if not self.canJumpOverOthers and not board.isPathClear(self.x, self.y, x, y):
            return False
        if ctrlCheck and board.wouldBeInCheck( self, x, y ):
            return False
        return True

    def canCapture(self, x: int, y: int, board, ctrlCheck=True):
        piece = board.getCell(x, y)
        if not piece or piece.player == self.player:
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
        if not self.canJumpOverOthers and not board.isPathClear(self.x, self.y, x, y):
            return False
        if ctrlCheck and board.wouldBeInCheck( self, x, y ):
            return False
        return True

    def getPossibleMoves( self, board ):
        res = []
        if self.possibleCaptureMoves != self.possibleRegularMoves:
            if self.multipleMove:
                for dir in self.possibleRegularMoves:
                    for k in range( -7, 7 ):
                        tox, toy = self.x + k * dir[ 0 ], self.y + k * dir[ 1 ]
                        if 0 <= tox < 8 and 0 <= toy < 8 and self.canMove( tox, toy, board ):
                            res.append( XY2POS( tox, toy ) )
                for dir in self.possibleCaptureMoves:
                    for k in range( -7, 7 ):
                        tox, toy = self.x + k * dir[ 0 ], self.y + k * dir[ 1 ]
                        if 0 <= tox < 8 and 0 <= toy < 8 and self.canCapture( tox, toy, board ):
                            res.append( XY2POS( tox, toy ) )
            else:
                for dir in self.possibleRegularMoves:
                    tox, toy = self.x + dir[ 0 ], self.y + dir[ 1 ]
                    if 0 <= tox < 8 and 0 <= toy < 8 and self.canMove( tox, toy, board ):
                        res.append( XY2POS( tox, toy ) )
                for dir in self.possibleCaptureMoves:
                    tox, toy = self.x + dir[ 0 ], self.y + dir[ 1 ]
                    if 0 <= tox < 8 and 0 <= toy < 8 and self.canCapture( tox, toy, board ):
                        res.append( XY2POS( tox, toy ) )
        else:
            if self.multipleMove:
                for dir in self.possibleRegularMoves:
                    for k in range( -7, 7 ):
                        tox, toy = self.x + k * dir[ 0 ], self.y + k * dir[ 1 ]
                        if 0 <= tox < 8 and 0 <= toy < 8 and ( self.canMove( tox, toy, board ) or self.canCapture( tox, toy, board ) ):
                            res.append( XY2POS( tox, toy ) )
            else:
                for dir in self.possibleRegularMoves:
                    tox, toy = self.x + dir[ 0 ], self.y + dir[ 1 ]
                    if 0 <= tox < 8 and 0 <= toy < 8 and ( self.canMove( tox, toy, board ) or self.canCapture( tox, toy, board ) ):
                        res.append( XY2POS( tox, toy ) )
        return list( set( res ) )

    def move( self, x, y ):
        self.x = x
        self.y = y
        self.moved = True

    def __str__( self ):
        return f'{"W" if self.player.color=="white" else "B"}{self.name}({XY2POS(self.x, self.y)})'
