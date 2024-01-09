from .ShatranjPiece import ShatranjPiece

class Horse( ShatranjPiece ):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.possibleRegularMoves = self.possibleCaptureMoves = [
            ( +1, +2 ), ( +2, +1 ),
            ( -1, +2 ), ( -2, +1 ),
            ( -1, -2 ), ( -2, -1 ),
            ( +1, -2 ), ( +2, -1 ),
        ]
        self.canJumpOverOthers = True
        self.multipleMove = False
        self.name = 'Horse'
        self.symbol = 'H'