from .helpers import POS2XY, XY2POS

class QirkatPiece:
    def __init__(self, player, pos):
        self.x, self.y = POS2XY( pos )
        self.player = player
        self.dirs = [ (-1, -1), (-1, +1), (+1, -1), (+1, +1), 
                      (-1, 0),  (+1, 0),  (0, -1),  (0, +1) ]
    
    def getPossibleDirections( self ):
        return self.dirs
    
    def getPossibleCaptures( self ):
        return [
            ( (-1, -1), (-2, -2) ),
            ( (-1, 1), (-2, 2) ),
            ( (1, 1), (2, 2) ),
            ( (1, -1), (2, -2) ),
            ( (-1, 0), (-2, 0) ),
            ( (+1, 0), (+2, 0) ),
            ( (0, -1), (0, -2) ),
            ( (0, +1), (0, +2) ),
        ]
    
    def __str__( self ):
        return f'{"W" if self.player.color=="white" else "B"}Checker({XY2POS(self.x, self.y)})'