from .ShatranjPiece import ShatranjPiece

class Fil(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.canJumpOverOthers = True
        self.possibleRegularMoves = self.possibleCaptureMoves = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        self.name = 'Fil'
        self.symbol = 'F'
