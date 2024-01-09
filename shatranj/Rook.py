from .ShatranjPiece import ShatranjPiece

class Rook(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = True
        self.canJumpOverOthers = False
        self.possibleRegularMoves = self.possibleCaptureMoves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.name = 'Rook'
        self.symbol = 'R'