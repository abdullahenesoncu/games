from .ShatranjPiece import ShatranjPiece

class Rook(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = True  # Rooks can move multiple squares in a straight line
        self.canJumpOverOthers = False  # Rooks cannot jump over other pieces
        self.possibleRegularMoves = self.possibleCaptureMoves = [
            (0, 1),  # Move up
            (1, 0),  # Move right
            (0, -1), # Move down
            (-1, 0)  # Move left
        ]
        self.name = 'Rook'  # Name of the piece
        self.symbol = 'R'  # Symbol representing the piece
