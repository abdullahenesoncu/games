class Player:
    def __init__(self, name, color):
        """
        Initialize a player with a name and color.
        :param name: The name of the player.
        :param color: The color of the player, either 'white' or 'black'.
        """
        self.name = name
        self.color = color  # 'white' or 'black'
        self.pieces = []  # Pieces that belong to the player

    def addPiece(self, piece):
        """Add a piece to the player's collection."""
        self.pieces.append(piece)

    def removePiece(self, piece):
        """Remove a piece from the player's collection."""
        if piece in self.pieces:
            self.pieces.remove(piece)
        else:
            raise ValueError(f"Piece {piece} not found in player's collection.")

    def __str__(self):
        """String representation of the player."""
        return f"{self.color}({self.name})"
