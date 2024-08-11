from .helpers import XY2POS, POS2XY
import math

class ShatranjPiece:
    def __init__(self, player, pos):
        self.x, self.y = POS2XY(pos)
        self.player = player
        self.possibleRegularMoves = None
        self.possibleCaptureMoves = None
        self.canJumpOverOthers = None
        self.multipleMove = None
        self.moved = False

    def _is_valid_move(self, x: int, y: int, board, ctrlCheck: bool, moves):
        """Common logic for move and capture checks."""
        if (x, y) == (self.x, self.y) or not (0 <= x < 8 and 0 <= y < 8):
            return False
        diff = (x - self.x, y - self.y)
        if not self.multipleMove:
            if diff not in moves:
                return False
        else:
            gcd = math.gcd(diff[0], diff[1])
            diff = (diff[0] // gcd, diff[1] // gcd)
            if diff not in moves:
                return False

        if not self.canJumpOverOthers and not board.isPathClear(self.x, self.y, x, y):
            return False
        if ctrlCheck and board.wouldBeInCheck(self, x, y):
            return False
        return True

    def canMove(self, x: int, y: int, board, ctrlCheck=True):
        """Check if the piece can move to the given position."""
        if board.getCell(x, y):  # If the target cell is occupied
            return False
        return self._is_valid_move(x, y, board, ctrlCheck, self.possibleRegularMoves)

    def canThreat(self, x: int, y: int, board, ctrlCheck=True):
        """Check if the piece can threaten the given position."""
        piece = board.getCell(x, y)
        if piece and piece.player == self.player:
            return False
        return self._is_valid_move(x, y, board, ctrlCheck, self.possibleCaptureMoves)

    def canCapture(self, x: int, y: int, board, ctrlCheck=True):
        """Check if the piece can capture the piece on the given position."""
        piece = board.getCell(x, y)
        if not piece or piece.player == self.player:
            return False
        return self._is_valid_move(x, y, board, ctrlCheck, self.possibleCaptureMoves)

    def getPossibleMoves(self, board):
        """Get all possible moves for the piece."""
        res = []

        def add_move_or_capture(dir, method):
            tox, toy = self.x + dir[0], self.y + dir[1]
            if 0 <= tox < 8 and 0 <= toy < 8 and method(tox, toy, board):
                res.append(XY2POS(tox, toy))

        if self.possibleCaptureMoves != self.possibleRegularMoves:
            if self.multipleMove:
                for dir in self.possibleRegularMoves:
                    for k in range(-7, 7):
                        add_move_or_capture((k * dir[0], k * dir[1]), self.canMove)
                for dir in self.possibleCaptureMoves:
                    for k in range(-7, 7):
                        add_move_or_capture((k * dir[0], k * dir[1]), self.canCapture)
            else:
                for dir in self.possibleRegularMoves:
                    add_move_or_capture(dir, self.canMove)
                for dir in self.possibleCaptureMoves:
                    add_move_or_capture(dir, self.canCapture)
        else:
            if self.multipleMove:
                for dir in self.possibleRegularMoves:
                    for k in range(-7, 7):
                        add_move_or_capture((k * dir[0], k * dir[1]), lambda x, y, board: self.canMove(x, y, board) or self.canCapture(x, y, board))
            else:
                for dir in self.possibleRegularMoves:
                    add_move_or_capture(dir, lambda x, y, board: self.canMove(x, y, board) or self.canCapture(x, y, board))

        return list(set(res))

    def move(self, x, y):
        """Move the piece to the given position."""
        self.x = x
        self.y = y
        self.moved = True

    def __str__(self):
        """String representation of the piece."""
        color = "W" if self.player.color == "white" else "B"
        return f'{color}{self.name}({XY2POS(self.x, self.y)})'
