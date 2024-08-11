from .ShatranjPiece import ShatranjPiece

class Fil(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.canJumpOverOthers = True  # The Fil can jump over other pieces
        # The Fil moves exactly two squares diagonally in any direction
        self.possibleRegularMoves = self.possibleCaptureMoves = [
            (2, 2),    # Move two squares diagonally up-right
            (2, -2),   # Move two squares diagonally down-right
            (-2, 2),   # Move two squares diagonally up-left
            (-2, -2)   # Move two squares diagonally down-left
        ]
        self.name = 'Fil'  # Name of the piece
        self.symbol = 'F'  # Symbol representing the piece
