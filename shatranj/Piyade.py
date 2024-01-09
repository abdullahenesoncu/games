from .ShatranjPiece import ShatranjPiece

class Piyade(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = False
        self.canJumpOverOthers = False
        self.direction = +1 if player.color == 'white' else -1
        self.possibleRegularMoves = [(0, self.direction)]
        self.possibleCaptureMoves = [(1, self.direction), (-1, self.direction)]
        self.name = 'Piyade'
        self.symbol = 'P'
