from .ChessPiece import ChessPiece

class Queen(ChessPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = True
        self.canJumpOverOthers = False
        self.possibleRegularMoves = self.possibleCaptureMoves = [
            (0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        self.name = 'Queen'
