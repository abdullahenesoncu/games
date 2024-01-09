from .ShatranjPiece import ShatranjPiece

class Vizier(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = False
        self.canJumpOverOthers = False
        self.possibleRegularMoves = self.possibleCaptureMoves = [ (1, 1), (1, -1), (-1, 1), (-1, -1) ]
        self.name = 'Vizier'
        self.symbol = 'V'
