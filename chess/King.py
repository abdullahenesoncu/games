from .ChessPiece import ChessPiece

class King(ChessPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = False
        self.canJumpOverOthers = False
        self.possibleRegularMoves = self.possibleCaptureMoves = [
            (0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        self.name = 'King'
    
    def canCastle(self, rook, board):
        if self.moved or rook.moved:
            return False
        if board.isCheck(self.player):
            return False
        if not board.isPathClear(self.x, self.y, rook.x, rook.y):
            return False

        direction = 1 if rook.x > self.x else -1
        checkRange = 3 if direction == -1 else 2  # 3 squares for queenside, 2 for kingside
        for i in range(1, checkRange):
            if board.isUnderAttack(self.x + i * direction, self.y, self.player):
                return False
        return True
    
    def castle(self, rook):
        if rook.x < self.x:  # Queenside castling
            kingX = rook.x + 2
            rookX = self.x - 1
        else:  # Kingside castling
            kingX = rook.x - 1
            rookX = self.x + 1

        self.move(kingX, self.y)
        rook.move(rookX, rook.y)
