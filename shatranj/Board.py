from .Piyade import Piyade
from .Rook import Rook
from .Horse import Horse
from .Fil import Fil
from .Vizier import Vizier
from .Shah import Shah
from .Player import Player
from .helpers import XY2POS, POS2XY

class Board:
    def __init__(self, player1, player2):
        self.pieces = []
        self.currentTurn = player1
        self.players = [player1, player2]
        self.halfMoveClock = 0
        self.fullMoveNumber = 1
        self.pieceMap = {}
        self.movementStack = []

    # Piece management methods
    def addPiece(self, piece):
        assert (piece.x, piece.y) not in self.pieceMap
        self.pieceMap[(piece.x, piece.y)] = piece
        self.pieces.append(piece)
        piece.player.addPiece(piece)

    def removePiece(self, piece):
        assert (piece.x, piece.y) in self.pieceMap
        self.pieces.remove(piece)
        piece.player.removePiece(piece)
        del self.pieceMap[(piece.x, piece.y)]

    def getCell(self, x, y):
        piece = self.pieceMap.get((x, y), None)
        if piece:
            assert piece.x == x and piece.y == y
        return piece

    # Movement-related methods
    def movePiece(self, piece, x, y):
        if piece.player != self.currentTurn:
            return False

        canMove = piece.canMove(x, y, self)
        canCapture = piece.canCapture(x, y, self)
        if not canMove and not canCapture:
            return False

        if self.wouldBeInCheck(piece, x, y):
            return False

        move = {
            'fromX': piece.x,
            'fromY': piece.y,
            'toX': x,
            'toY': y,
            'halfMoveClock': self.halfMoveClock,
            'fullMoveNumber': self.fullMoveNumber,
            'capturedPieceType': None,
            'promoted': False,
        }

        captured_piece = self.getCell(x, y)
        if captured_piece and canCapture:
            self.removePiece(captured_piece)
            move['capturedPieceType'] = type(captured_piece)

        self.removePiece(piece)
        piece.move(x, y)
        self.addPiece(piece)

        if isinstance(piece, Piyade) and (piece.y == 0 or piece.y == 7):
            promoted_piece = self.promotePiyade(piece)
            self.removePiece(piece)
            self.addPiece(promoted_piece)
            move['promoted'] = True

        self.moveSuccesful(piece, move)
        return True

    def moveSuccesful(self, piece, move):
        if isinstance(piece, Piyade) or move['capturedPieceType'] is not None:
            self.halfMoveClock = 0
        else:
            self.halfMoveClock += 1

        if self.currentTurn.color == 'black':
            self.fullMoveNumber += 1

        self.movementStack.append(move)
        self.switchTurn()

    def undo(self):
        if not self.movementStack:
            return False

        move = self.movementStack.pop()
        piece = self.getCell(move['toX'], move['toY'])
        self.removePiece(piece)
        piece.x, piece.y = move['fromX'], move['fromY']
        self.addPiece(piece)

        if move['capturedPieceType'] is not None:
            captured_piece = move['capturedPieceType'](self.currentTurn, XY2POS(move['toX'], move['toY']))
            captured_piece.x, captured_piece.y = move['toX'], move['toY']
            self.addPiece(captured_piece)

        if move['promoted']:
            self.removePiece(piece)
            original_piyade = Piyade(self.opponent(self.currentTurn), XY2POS(move['fromX'], move['fromY']))
            self.addPiece(original_piyade)

        self.currentTurn = self.opponent(self.currentTurn)
        self.halfMoveClock = move['halfMoveClock']
        self.fullMoveNumber = move['fullMoveNumber']

        return True

    # Game state methods
    def switchTurn(self):
        self.currentTurn = self.opponent(self.currentTurn)

    def isPathClear(self, x1: int, y1: int, x2: int, y2: int):
        if x1 == x2:
            stepX, stepY = 0, 1 if y1 < y2 else -1
        elif y1 == y2:
            stepY, stepX = 0, 1 if x1 < x2 else -1
        else:
            stepX = 1 if x1 < x2 else -1
            stepY = 1 if y1 < y2 else -1

        curX, curY = x1 + stepX, y1 + stepY
        while curX != x2 or curY != y2:
            if self.getCell(curX, curY):
                return False
            curX += stepX
            curY += stepY
        return True

    def isUnderAttack(self, x, y, player):
        opponent = self.opponent(player)
        for p in opponent.pieces:
            if p.canThreat(x, y, self):
                return True
        return False

    def isCheck(self, player=None):
        player = player or self.currentTurn
        shah = next((p for p in player.pieces if isinstance(p, Shah)), None)
        if not shah:
            return False

        opponent = self.opponent(player)
        for p in opponent.pieces:
            if p.canCapture(shah.x, shah.y, self, ctrlCheck=False):
                return True
        return False

    def wouldBeInCheck(self, piece, x, y):
        tmpx, tmpy = piece.x, piece.y
        self.removePiece(piece)
        capturedPiece = self.getCell(x, y)
        if capturedPiece:
            self.removePiece(capturedPiece)

        piece.x = x
        piece.y = y
        self.addPiece(piece)

        ret = self.isCheck()

        self.removePiece(piece)
        piece.x = tmpx
        piece.y = tmpy
        self.addPiece(piece)
        if capturedPiece:
            self.addPiece(capturedPiece)

        return ret

    def isCheckmate(self):
        if not self.isCheck():
            return False
        piecePosition = [(p.x, p.y) for p in self.currentTurn.pieces]
        for piecePos in piecePosition:
            piece = self.getCell(*piecePos)
            for x in range(8):
                for y in range(8):
                    if (piece.canMove(x, y, self, ctrlCheck=False) or piece.canCapture(x, y, self, ctrlCheck=False)) and not self.wouldBeInCheck(piece, x, y):
                        return False
        return True

    def isGameOver(self):
        return self.isStalemate() or self.isCheckmate() or self.isDraw()

    def winner(self):
        if self.isDraw():
            return None
        if self.isStalemate():
            return self.opponent(self.currentTurn)
        if self.isCheckmate():
            return self.opponent(self.currentTurn)
        return self.currentTurn

    def isStalemate(self):
        if self.isCheck():
            return False
        for piece in self.currentTurn.pieces:
            for x in range(8):
                for y in range(8):
                    if piece.canMove(x, y, self, ctrlCheck=False) and not self.wouldBeInCheck(piece, x, y):
                        return False
        return True

    def isDraw(self):
        if len(self.pieces) == 2 and all(isinstance(piece, Shah) for piece in self.pieces):
            return True

        piecesCurrent = self.currentTurn.pieces
        piecesOpponent = self.opponent(self.currentTurn).pieces
        if len(piecesCurrent) == 1 and len(piecesOpponent) == 2 and (
            piecesCurrent[0].canCapture(piecesOpponent[0].x, piecesOpponent[0].y, self) or
            piecesCurrent[0].canCapture(piecesOpponent[1].x, piecesOpponent[1].y, self)
        ):
            return True

        if len(self.pieces) == 3:
            shahs = [piece for piece in self.pieces if isinstance(piece, Shah)]
            others = [piece for piece in self.pieces if not isinstance(piece, Shah)]
            if len(shahs) == 2 and (isinstance(others[0], Fil) or isinstance(others[0], Horse)):
                return True

        return False

    def opponent(self, player):
        return self.players[0] if player == self.players[1] else self.players[1]

    # Utility methods
    def promotePiyade(self, piyade):
        x, y = piyade.x, piyade.y
        return Vizier(piyade.player, XY2POS(x, y))

    def getPossibleMoves(self):
        res = []
        if self.isGameOver():
            return res
        pieces = [p for p in self.pieces]
        for piece in pieces:
            if piece.player != self.currentTurn:
                continue
            res += [XY2POS(piece.x, piece.y) + m for m in piece.getPossibleMoves(self)]
        return res

    def parseInput(self, move):
        if len(move) == 4:
            return move[:2], move[2:4]
        else:
            return None

    def play(self, move):
        from_pos, to_pos = self.parseInput(move)
        from_pos = POS2XY(from_pos)
        to_pos = POS2XY(to_pos)

        piece = self.getCell(*from_pos)
        if not piece or piece.player != self.currentTurn:
            return False

        return self.movePiece(piece, *to_pos)

    def boardToString(self):
        board = [['.' for _ in range(8)] for _ in range(8)]
        for piece in self.pieces:
            symbol = piece.symbol.upper() if piece.player.color == 'white' else piece.symbol.lower()
            board[7 - piece.y][piece.x] = symbol

        board_with_labels = ['  a b c d e f g h']
        for i, row in enumerate(board):
            row_label = f'{8 - i} ' + ' '.join(row)
            board_with_labels.append(row_label)

        return '\n'.join(board_with_labels)

    def boardToFEN(self):
        fen = ""
        for y in range(8, 0, -1):
            empty = 0
            for x in range(8):
                piece = self.getCell(x, y - 1)
                if piece:
                    if empty:
                        fen += str(empty)
                        empty = 0
                    fen += piece.symbol.upper() if piece.player.color == 'white' else piece.symbol.lower()
                else:
                    empty += 1
            if empty:
                fen += str(empty)
            if y > 1:
                fen += '/'
        fen += ' w' if self.currentTurn.color == 'white' else ' b'
        fen += ' ' + str(self.halfMoveClock)
        fen += ' ' + str(self.fullMoveNumber)
        return fen

    @classmethod
    def boardFromFEN(cls, fen):
        fields = fen.split()
        if len(fields) != 4:
            raise ValueError("Invalid FEN string")

        player1 = Player('White', 'white')
        player2 = Player('Black', 'black')
        board = cls(player1, player2)

        for y, row in enumerate(fields[0].split('/')):
            x = 0
            for char in row:
                if char.isdigit():
                    x += int(char)
                else:
                    color = 'white' if char.isupper() else 'black'
                    player = player1 if color == 'white' else player2
                    piece_class = cls.getPieceClassFromFEN(char)
                    piece = piece_class(player, XY2POS(x, 7 - y))
                    if piece_class == Piyade and (color == 'white' and y != 6 or color == 'black' and y != 1):
                        piece.moved = True
                    board.addPiece(piece)
                    x += 1

        board.currentTurn = player1 if fields[1] == 'w' else player2
        board.halfMoveClock = int(fields[2])
        board.fullMoveNumber = int(fields[3])

        return board

    @classmethod
    def getPieceClassFromFEN(cls, char):
        piece_map = {
            'p': Piyade, 'r': Rook, 'h': Horse,
            'f': Fil, 'v': Vizier, 's': Shah
        }
        return piece_map[char.lower()]

    @classmethod
    def getInitialRepr(cls):
        return 'rhfvsfhr/pppppppp/8/8/8/8/PPPPPPPP/RHFVSFHR w 0 1'

    @classmethod
    def extension(cls, func):
        setattr(cls, func.__name__, func)
        return func
