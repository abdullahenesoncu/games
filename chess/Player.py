class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color  # 'white' or 'black'
        self.pieces = []  # Pieces that belong to the player

    def addPiece(self, piece):
        self.pieces.append(piece)

    def removePiece(self, piece):
        assert piece in self.pieces
        self.pieces.remove(piece)
