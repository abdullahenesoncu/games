from .ShatranjPiece import ShatranjPiece

class Horse(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        # The Horse (Knight) can move in an "L" shape, so it has 8 possible moves
        self.possibleRegularMoves = self.possibleCaptureMoves = [
            (+1, +2), (+2, +1),
            (-1, +2), (-2, +1),
            (-1, -2), (-2, -1),
            (+1, -2), (+2, -1),
        ]
        self.canJumpOverOthers = True  # Knights can jump over other pieces
        self.multipleMove = False  # Knights move only one step at a time
        self.name = 'Horse'  # Name of the piece
        self.symbol = 'H'  # Symbol representing the piece
