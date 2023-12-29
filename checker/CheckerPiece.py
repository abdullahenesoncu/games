from .helpers import POS2XY, XY2POS

class CheckerPiece:
    def __init__(self, player, pos, king=False):
        self.x, self.y = POS2XY( pos )
        self.player = player
        self.king = king
        self.direction = +1 if player.color == 'white' else -1
        self.dirs = [ (-1, -1), (-1, +1), (+1, -1), (+1, +1) ]
    
    def canMoveBack( self ):
        return self.king
    
    def getPossibleDirections( self ):
        return self.dirs if self.canMoveBack() else [ dir for dir in self.dirs if dir[ 1 ] == self.direction ]
    
    def getPossibleCaptures( self ):
        return [
            ( (-1, -1), (-2, -2) ),
            ( (-1, 1), (-2, 2) ),
            ( (1, 1), (2, 2) ),
            ( (1, -1), (2, -2) ),
        ]
    
    def __str__( self ):
        return f'{"W" if self.player.color=="white" else "B"}{"King" if self.king else "Checker"}({XY2POS(self.x, self.y)})'