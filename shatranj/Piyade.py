from .ShatranjPiece import ShatranjPiece

class Piyade(ShatranjPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = False  # Pawns cannot make multiple moves at once
        self.canJumpOverOthers = False  # Pawns cannot jump over other pieces
        self.direction = 1 if player.color == 'white' else -1  # Determine movement direction based on player color
        self.possibleRegularMoves = [(0, self.direction)]  # Pawns move forward
        self.possibleCaptureMoves = [(1, self.direction), (-1, self.direction)]  # Pawns capture diagonally
        self.name = 'Piyade'  # Name of the piece
        self.symbol = 'P'  # Symbol representing the piece
