from .ShatranjPiece import ShatranjPiece

class Vizier(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = False  # Vizier can only move one square at a time
        self.canJumpOverOthers = False  # Vizier cannot jump over other pieces
        # Vizier moves diagonally one square in any direction
        self.possibleRegularMoves = self.possibleCaptureMoves = [
            (1, 1),    # Move one square diagonally up-right
            (1, -1),   # Move one square diagonally down-right
            (-1, 1),   # Move one square diagonally up-left
            (-1, -1)   # Move one square diagonally down-left
        ]
        self.name = 'Vizier'  # Name of the piece
        self.symbol = 'V'  # Symbol representing the piece
