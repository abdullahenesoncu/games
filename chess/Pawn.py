from .ChessPiece import ChessPiece

class Pawn(ChessPiece):
    def __init__(self, player, pos):
        super().__init__(player, pos)
        self.multipleMove = False
        self.canJumpOverOthers = False
        self.direction = +1 if player.color == 'white' else -1
        self.possibleRegularMoves = [(0, self.direction)]
        self.possibleCaptureMoves = [(1, self.direction), (-1, self.direction)]
        self.name = 'Pawn'

    def canMove(self, x: int, y: int, board, ctrlCheck=True):
        if board.getCell( x, y ):
            return False
        if not self.moved and (x - self.x, y - self.y) == (0, 2 * self.direction):
            if board.wouldBeInCheck( self, x, y ):
                return False
            if board.isPathClear(self.x, self.y, x, y):
                return True
        
        # En Passant Condition
        if self.canEnpassant(x, y, board):
            return True

        return super().canMove(x, y, board, ctrlCheck=ctrlCheck)
    
    def canEnpassant(self, x: int, y: int, board):
        if board.lastMove is None:
            return False

        last_move_info = board.lastMove
        last_piece = last_move_info["moved_piece"]
        last_from_pos = last_move_info["from_pos"]
        last_to_pos = last_move_info["to_pos"]

        if not isinstance(last_piece, Pawn):
            return False
        
        last_x_from, last_y_from = last_from_pos
        last_x_to, last_y_to = last_to_pos

        # Check if the last move was a double step from the starting position
        if abs(last_y_to - last_y_from) == 2 and last_y_to == self.y:
            if x == last_x_to and y == self.y + self.direction and board.getCell(last_x_to, last_y_to+self.direction) is None:
                return True
        return False

    def enpassant(self, x: int, y: int, board):
        last_move_info = board.lastMove
        last_piece = last_move_info["moved_piece"]
        if last_piece not in board.pieces:
            print(board.lastMove)

        board.pieces.remove(last_piece)
        last_piece.player.removePiece(last_piece)
        self.move(x, y)
