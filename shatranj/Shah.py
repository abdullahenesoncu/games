from .ShatranjPiece import ShatranjPiece

class Shah(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = False  # The Shah (King) can only move one square at a time
        self.canJumpOverOthers = False  # The Shah cannot jump over other pieces
        # The Shah can move one square in any direction
        self.possibleRegularMoves = self.possibleCaptureMoves = [
            (0, 1),   # Move one square up
            (1, 0),   # Move one square right
            (0, -1),  # Move one square down
            (-1, 0),  # Move one square left
            (1, 1),   # Move one square diagonally up-right
            (1, -1),  # Move one square diagonally down-right
            (-1, 1),  # Move one square diagonally up-left
            (-1, -1)  # Move one square diagonally down-left
        ]
        self.name = 'Shah'  # Name of the piece
        self.symbol = 'S'  # Symbol representing the piece
