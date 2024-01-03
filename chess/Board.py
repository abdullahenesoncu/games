from .Pawn import Pawn
from .Rook import Rook
from .Knight import Knight
from .Bishop import Bishop
from .Queen import Queen
from .King import King
from .Player import Player
from .helpers import XY2POS, POS2XY

class Board:
    def __init__(self, player1, player2):
        self.pieces = []
        self.currentTurn = player1
        self.players = [player1, player2]
        self.lastMove = None
        self.halfMoveClock = 0
        self.fullMoveNumber = 1

    def addPiece(self, piece):
        self.pieces.append(piece)
        piece.player.addPiece(piece)

    def getCell(self, x, y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None
    
    def moveSuccesful( self, piece, targetPiece, fromX, fromY, toX, toY ):
        self.lastMove = {
            "moved_piece": piece,
            "from_pos": (fromX, fromY),
            "to_pos": (toX, toY),
            "captured_piece": targetPiece,
            "prev_half_move_clock": self.halfMoveClock,
            "prev_full_move_number": self.fullMoveNumber,
        }
        if isinstance(piece, Pawn) or targetPiece is not None:
            self.halfMoveClock = 0
        else:
            self.halfMoveClock += 1
        
        if self.currentTurn.color == 'black':
            self.fullMoveNumber += 1
        
        self.switchTurn()

    def movePiece(self, piece, x, y, additionalInput=None):
        if piece.player != self.currentTurn:
            return False
        
        fromX = piece.x
        fromY = piece.y
        toX = x
        toY = y
        targetPiece = self.getCell( x, y )

        # Castle Move
        if isinstance(piece, King) and abs(x - piece.x) == 2:
            rookPos = (0, piece.y) if x < piece.x else (7, piece.y)
            rook = self.getCell(*rookPos)
            if rook and piece.canCastle(rook, self):
                piece.castle(rook)
                self.moveSuccesful( piece, targetPiece, fromX, fromY, toX, toY )
                return True
        
        # Enpassant
        if isinstance(piece, Pawn) and piece.canEnpassant(x, y, self):
            piece.enpassant(x, y, self)
            self.moveSuccesful( piece, targetPiece, fromX, fromY, toX, toY )
            return True
        
        # Normal Move
        canMove = piece.canMove(x, y, self)
        canCapture = piece.canCapture(x, y, self)
        if not canMove and not canCapture:
            return False

        # Check if the move puts or leaves the player's king in check
        if self.wouldBeInCheck(piece, x, y):
            return False  # Cannot make a move that puts/keeps the king in check

        # Move the piece and handle captures
        captured_piece = self.getCell(x, y)
        if captured_piece and canCapture:
            self.pieces.remove(captured_piece)
            captured_piece.player.removePiece(captured_piece)
        piece.move( x, y )

        # Pawn Promotion Logic
        if isinstance(piece, Pawn) and (piece.y == 0 or piece.y == 7):
            promoted_piece = self.promotePawn(piece, additionalInput)
            if promoted_piece:
                self.pieces.append(promoted_piece)
                piece.player.pieces.append(promoted_piece)
                self.pieces.remove(piece)
                piece.player.pieces.remove(piece)

        self.moveSuccesful( piece, targetPiece, fromX, fromY, toX, toY )
        return True

    def promotePawn(self, pawn, additionalInput):
        if not additionalInput:
            return None

        additionalInput = additionalInput.lower()
        x, y = pawn.x, pawn.y

        if additionalInput in [ 'q', 'queen' ]:
            return Queen(pawn.player, XY2POS(x, y))
        elif additionalInput in [ 'r', 'rook' ]:
            return Rook(pawn.player, XY2POS(x, y))
        elif additionalInput in [ 'b', 'bishop' ]:
            return Bishop(pawn.player, XY2POS(x, y))
        elif additionalInput in [ 'n', 'knight' ]:
            return Knight(pawn.player, XY2POS(x, y))
        else:
            return None

    def wouldBeInCheck(self, piece, x, y):
        original_x, original_y = piece.x, piece.y
        capturedPiece = self.getCell( x, y )
        if capturedPiece:
            capturedPiece.player.pieces.remove( capturedPiece )
            self.pieces.remove( capturedPiece )

        piece.x, piece.y = x, y
        inCheck = self.isCheck(piece.player)

        piece.x, piece.y = original_x, original_y
        if capturedPiece:
            capturedPiece.player.pieces.append( capturedPiece )
            self.pieces.append( capturedPiece )
        
        return inCheck

    def isCheck(self, player):
        king = next((p for p in player.pieces if isinstance(p, King)), None)
        if not king:
            return False

        opponent = self.players[0] if player == self.players[1] else self.players[1]
        for p in opponent.pieces:
            if p.canCapture(king.x, king.y, self, ctrlCheck=False):
                return True
        return False

    def isCheckmate(self, player):
        if not self.isCheck(player):
            return False
        for piece in player.pieces:
            for x in range(8):
                for y in range(8):
                    if ( piece.canMove(x, y, self, ctrlCheck=False) or piece.canCapture(x, y, self, ctrlCheck=False) ) and not self.wouldBeInCheck(piece, x, y):
                        return False
        return True

    def isGameOver(self):
        if self.isCheckmate(self.currentTurn) or self.isDraw():
            return True
        return False

    def isDraw(self):
        # Checking for two kings condition
        if len(self.pieces) == 2 and all(isinstance(piece, King) for piece in self.pieces):
            return True

        # Checking for king and bishop/knight against king condition
        if len(self.pieces) == 3:
            kings = [piece for piece in self.pieces if isinstance(piece, King)]
            others = [piece for piece in self.pieces if not isinstance(piece, King)]
            if len(kings) == 2 and (isinstance(others[0], Bishop) or isinstance(others[0], Knight)):
                return True

        # Checking for stalemate condition
        current_player = self.currentTurn
        if self.isStalemate(current_player):
            return True

        return False
    
    def isStalemate(self, player):
        if self.isCheck(player):
            return False  # Not a stalemate if the player is in check

        for piece in player.pieces:
            for x in range(8):
                for y in range(8):
                    if piece.canMove(x, y, self) and not self.wouldBeInCheck(piece, x, y):
                        return False  # Found a legal move, so not a stalemate
        return True

    def switchTurn(self):
        self.currentTurn = self.players[0] if self.currentTurn == self.players[1] else self.players[1] 
    
    def isPathClear(self, x1: int, y1: int, x2: int, y2: int):
        if x1 == x2:
            stepX = 0
            stepY = 1 if y1 < y2 else -1
        elif y1 == y2:
            stepY = 0
            stepX = 1 if x1 < x2 else -1
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
        opponent = self.players[0] if player == self.players[1] else self.players[1]
        for p in opponent.pieces:
            if p.canThreat(x, y, self):
                return True
        return False

    def play( self, from_pos, to_pos, additionalInput=None ):
        from_pos = POS2XY( from_pos )
        to_pos = POS2XY( to_pos )
        if not from_pos or not to_pos:
            return False
        
        piece = self.getCell(*from_pos)
        if not piece or piece.player != self.currentTurn:
            return False
        
        return self.movePiece(piece, *to_pos, additionalInput)
    
    def getCastlingAvailability(self):
        castling = ''
        for player in self.players:
            king = next((p for p in player.pieces if isinstance(p, King)), None)
            if king and not king.moved:
                ks_rook = next((p for p in player.pieces if isinstance(p, Rook) and p.x == 7), None)
                qs_rook = next((p for p in player.pieces if isinstance(p, Rook) and p.x == 0), None)
                if ks_rook and not ks_rook.moved:
                    castling += 'K' if player.color == 'white' else 'k'
                if qs_rook and not qs_rook.moved:
                    castling += 'Q' if player.color == 'white' else 'q'
        return castling or '-'

    def setCastlingAvailability(self, castling_field):
        for piece in self.pieces:
            if isinstance(piece, King) or isinstance(piece, Rook):
                piece.moved = True  # Initially set all to moved
                if isinstance(piece, King):
                    if (piece.player.color == 'white' and 'K' in castling_field) or \
                       (piece.player.color == 'black' and 'k' in castling_field):
                        piece.moved = False
                    if (piece.player.color == 'white' and 'Q' in castling_field) or \
                       (piece.player.color == 'black' and 'q' in castling_field):
                        piece.moved = False
                elif isinstance(piece, Rook):
                    if (piece.player.color == 'white' and 'Q' in castling_field and piece.x == 0) or \
                       (piece.player.color == 'black' and 'q' in castling_field and piece.x == 0):
                        piece.moved = False
                    if (piece.player.color == 'white' and 'K' in castling_field and piece.x == 7) or \
                       (piece.player.color == 'black' and 'k' in castling_field and piece.x == 7):
                        piece.moved = False

    def getEnPassantTarget(self):
        if self.lastMove and isinstance(self.lastMove["moved_piece"], Pawn):
            from_x, from_y = self.lastMove["from_pos"]
            to_x, to_y = self.lastMove["to_pos"]
            if abs(to_y - from_y) == 2:
                target_y = (from_y + to_y) // 2
                return XY2POS(to_x, target_y)
        return '-'
    
    def boardToString(self):
        # Initialize an 8x8 matrix with dots
        board = [['.' for _ in range(8)] for _ in range(8)]

        # Piece symbols
        piece_symbols = {
            Pawn: 'p', Knight: 'n', Bishop: 'b', Rook: 'r', Queen: 'q', King: 'k'
        }

        # Place pieces on the board
        for piece in self.pieces:
            symbol = piece_symbols[type(piece)].upper() if piece.player.color == 'white' else piece_symbols[type(piece)].lower()
            board[7 - piece.y][piece.x] = symbol  # Adjust for 0-indexing and flip y-axis

        # Add row and column labels
        board_with_labels = ['  a b c d e f g h']
        for i, row in enumerate(board):
            row_label = f'{8 - i} ' + ' '.join(row)  # Adjust for 0-indexing and flip y-axis
            board_with_labels.append(row_label)

        return '\n'.join(board_with_labels)

    def boardToFEN(self):
        piece_symbols = {
            Pawn: 'p', Knight: 'n', Bishop: 'b', Rook: 'r', Queen: 'q', King: 'k'
        }
        fen = ""
        for y in range( 8, 0, -1 ):
            empty = 0
            for x in range( 8 ):
                piece = self.getCell( x, y - 1 )
                if piece:
                    if empty:
                        fen += str( empty )
                        empty = 0
                    fen += piece_symbols.get( type( piece ) ).upper() if piece.player.color == 'white' else piece_symbols.get( type( piece ) ).lower()
                else:
                    empty += 1
            if empty:
                fen += str( empty )
            if y > 1:
                fen += '/'
        fen += ' w' if self.currentTurn.color == 'white' else ' b'
        fen += ' ' + self.getCastlingAvailability()
        fen += ' ' + self.getEnPassantTarget()
        fen += ' ' + str( self.halfMoveClock )
        fen += ' ' + str( self.fullMoveNumber )
        return fen
    
    @classmethod
    def load( cls, board_string ):
        chessboard = Board( Player('White', 'white'), Player('Black', 'black') )
        rows = board_string.strip().split('\n')
        chessboard.pieces = []

        piece_classes = {
            'p': Pawn, 'r': Rook, 'n': Knight,
            'b': Bishop, 'q': Queen, 'k': King
        }

        for i, row in enumerate(rows[1:], 1):
            cols = row.split()[1:]
            for j, symbol in enumerate(cols):
                if symbol != '.':
                    color = 'white' if symbol.isupper() else 'black'
                    player = [ player for player in chessboard.players if player.color == color ][ 0 ]
                    piece_class = piece_classes[symbol.lower()]
                    piece = piece_class(player, XY2POS(j, 8 - i))
                    chessboard.addPiece(piece)
        return chessboard
    
    @classmethod
    def boardFromFEN(cls, fen):
        fields = fen.split()
        if len(fields) != 6:
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
                    if piece_class == Pawn and (color == 'white' and y != 6 or color == 'black' and y != 1):
                        piece.moved = True
                    board.addPiece(piece)
                    x += 1

        board.currentTurn = player1 if fields[1] == 'w' else player2
        board.setCastlingAvailability(fields[2])

        en_passant_field = fields[3]
        if en_passant_field != '-':
            en_passant_pos = POS2XY(en_passant_field)
            pawn_y = 3 if en_passant_pos[1] == 2 else 4
            pawn_x = en_passant_pos[0]
            pawn = board.getCell(pawn_x, pawn_y)
            if pawn and isinstance(pawn, Pawn):
                last_move_from = (pawn_x, pawn_y - pawn.direction * 2)
                last_move_to = (pawn_x, pawn_y)
                board.lastMove = {
                    "moved_piece": pawn,
                    "from_pos": last_move_from,
                    "to_pos": last_move_to,
                    "captured_piece": None,  # No piece is captured in en passant setup
                    "prev_half_move_clock": None,  # Previous half move clock not known from FEN
                    "prev_full_move_number": None  # Previous full move number not known from FEN
                }
        else:
            board.lastMove = None

        board.halfMoveClock = int(fields[4])
        board.fullMoveNumber = int(fields[5])

        return board

    @classmethod
    def getPieceClassFromFEN(cls, char):
        piece_map = {
            'p': Pawn, 'r': Rook, 'n': Knight,
            'b': Bishop, 'q': Queen, 'k': King
        }
        return piece_map[char.lower()]
