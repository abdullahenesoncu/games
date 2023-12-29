from .ChessPiece import ChessPiece

class Bishop(ChessPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = True
        self.canJumpOverOthers = False
        self.possibleRegularMoves = self.possibleCaptureMoves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.name = 'Bishop'
