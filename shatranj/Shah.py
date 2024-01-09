from .ShatranjPiece import ShatranjPiece

class Shah(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = False
        self.canJumpOverOthers = False
        self.possibleRegularMoves = self.possibleCaptureMoves = [
            (0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        self.name = 'Shah'
        self.symbol = 'S'
