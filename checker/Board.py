from .helpers import XY2POS, POS2XY
from .Player import Player
from .CheckerPiece import CheckerPiece

class Board:
    def __init__( self, player1, player2 ):
        self.pieces = []
        self.currentTurn = player1
        self.players = [player1, player2]
        self.pieceToPlay = None
        self.rows = 8
        self.columns = 8

    def addPiece( self, piece ):
        self.pieces.append(piece)
        piece.player.addPiece(piece)

    def getCell( self, x, y ):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None
    
    def canMove( self, piece, x, y ):
        if piece.player != self.currentTurn:
            return False
        if self.pieceToPlay and self.pieceToPlay != piece:
            return False
        if x < 0 or x >= self.columns or y < 0 or y >= self.rows:
            return False
        maxCaptures = self.findCapturesFromPosition(piece, piece.x, piece.y)
        if not self.pieceToPlay and self.findMaxCapturesForCurrentPlayer() != maxCaptures:
            return False
        if not self.pieceToPlay and maxCaptures == 0:
            if ( x-piece.x, y-piece.y ) in piece.getPossibleDirections() and self.getCell(x, y) is None:
                return True
        for ( cx, cy ), ( gx, gy ) in piece.getPossibleCaptures():
            if gx == x - piece.x and gy == y - piece.y:
                if self.getCell( x, y ):
                    return False
                c = self.getCell( piece.x + cx, piece.y + cy ) 
                if c is None or c.player == self.currentTurn:
                    return False
                ox = piece.x
                oy = piece.y
                capturedPiece, _ = self.simulateCapture(piece, x, y, piece.x+cx, piece.y+cy)
                nextMaxCaptures = self.findCapturesFromPosition(piece, x, y)
                self.undoCapture(piece, capturedPiece, (ox, oy))
                if maxCaptures != nextMaxCaptures + 1:
                    print(maxCaptures , XY2POS(ox,oy), XY2POS(x,y), nextMaxCaptures)
                    return False
                return True
        return False
    
    def move( self, piece, x, y ):
        if not self.canMove( piece, x, y ):
            return False
        if ( x-piece.x, y-piece.y ) in piece.getPossibleDirections() and self.getCell(x, y) is None:
            piece.x = x
            piece.y = y
            if piece.direction == 1 and piece.y == 7:
                piece.king = True
            if piece.direction == -1 and piece.y == 0:
                piece.king = True
            self.switchTurn()
            return True
        for ( cx, cy ), ( gx, gy ) in piece.getPossibleCaptures():
            if gx == x - piece.x and gy == y - piece.y:
                self.simulateCapture(piece, piece.x+gx, piece.y+gy, piece.x+cx, piece.y+cy)
                maxCaptures = self.findCapturesFromPosition(piece, piece.x, piece.y)
                if piece.direction == 1 and piece.y == 7:
                    piece.king = True
                if piece.direction == -1 and piece.y == 0:
                    piece.king = True
                if not maxCaptures:
                    self.switchTurn()
                else:
                    self.pieceToPlay = piece
                return True
        return False
    
    def switchTurn(self):
        self.pieceToPlay = None
        self.currentTurn = self.players[0] if self.currentTurn == self.players[1] else self.players[1] 

    def simulateCapture(self, piece, jump_x, jump_y, capture_x, capture_y):
        captured_piece = self.getCell(capture_x, capture_y)
        self.pieces.remove(captured_piece)
        captured_piece.player.pieces.remove(captured_piece)
        piece.x, piece.y = jump_x, jump_y
        return captured_piece, (piece.x, piece.y)

    def undoCapture(self, piece, captured_piece, original_position):
        piece.x, piece.y = original_position
        self.pieces.append(captured_piece)
        captured_piece.player.pieces.append(captured_piece)

    def findCapturesFromPosition(self, piece, x, y):
        max_captures = 0

        for (dx, dy), (gx, gy) in piece.getPossibleCaptures():
            capture_x, capture_y = x + dx, y + dy
            jump_x, jump_y = x + gx, y + gy
            if jump_x<0 or jump_x>=self.columns or jump_y<0 or jump_y>=self.rows: continue
            if self.getCell(jump_x, jump_y) is None and self.getCell(capture_x, capture_y) and self.getCell(capture_x, capture_y).player.color != piece.player.color:
                ox, oy = piece.x, piece.y
                captured_piece, new_position = self.simulateCapture(piece, jump_x, jump_y, capture_x, capture_y)
                captures = 1 + self.findCapturesFromPosition(piece, jump_x, jump_y)
                self.undoCapture(piece, captured_piece, (ox, oy))
                max_captures = max(max_captures, captures)

        return max_captures

    def findMaxCapturesForCurrentPlayer(self):
        max_captures = 0

        for piece in self.pieces:
            if piece.player == self.currentTurn:
                captures = self.findCapturesFromPosition(piece, piece.x, piece.y)
                max_captures = max(max_captures, captures)

        return max_captures
    
    def isDraw(self):
        if len(self.pieces) == 2 and all(piece.king for piece in self.pieces):
            return True
        return False
    
    def isGameOver(self):
        if not any(piece.player == self.currentTurn for piece in self.pieces):
            return True
        if ( not any(self.canMove(piece, piece.x + dx, piece.y + dy) for piece in self.pieces for dx, dy in piece.getPossibleDirections()) and
             not any(self.canMove(piece, piece.x + gx, piece.y + gy) for piece in self.pieces for (cx, cy), (gx, gy) in piece.getPossibleCaptures())):
            return True
        return False
    
    def play( self, from_pos, to_pos ):
        from_pos = POS2XY( from_pos )
        to_pos = POS2XY( to_pos )
        if not from_pos or not to_pos:
            return False
        
        piece = self.getCell(*from_pos)
        if not piece or piece.player != self.currentTurn:
            return False
        
        return self.move(piece, *to_pos)
    
    @classmethod
    def loadFEN( cls, fen ):
        'c1c1c1c1/1c1c1c1c/c1c1c1c1/8/8/1C1C1C1C/C1C1C1C1/1C1C1C1C w -'
        repr, color, cell = fen.split()
        player1 = Player( 'White', 'white' )
        player2 = Player( 'Black', 'black' )
        checkerboard = cls( player1, player2 )
        assert( len( repr.split( '/' ) ) == 8 )
        for y, line in enumerate( repr.split( '/' ) ):
            x = 0
            for c in line:
                if c.isnumeric():
                    x += int(c)
                else:
                    if c == c.lower():
                        checkerboard.addPiece( CheckerPiece( player2, XY2POS( x, 7-y ), c=='k' ) )
                    else:
                        checkerboard.addPiece( CheckerPiece( player1, XY2POS( x, 7-y ), c=='K' ) )
                    x += 1
        checkerboard.currentTurn = player1 if color == 'w' else player2
        checkerboard.pieceToPlay = None if cell == '-' else checkerboard.getCell( *POS2XY( cell ) )
        return checkerboard
    
    def dumpFEN( self ):
        board_repr = []
        for j in reversed( range( 8 ) ):
            empty_count = 0
            row_repr = ''
            for i in range( 8 ):
                piece = self.getCell( i, j )
                if not piece:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_repr += str( empty_count )
                        empty_count = 0
                    if piece.player.color == 'white':
                        if piece.king: row_repr += 'K'
                        else: row_repr += 'C'
                    else:
                        if piece.king: row_repr += 'k'
                        else: row_repr += 'c'
            if empty_count > 0:
                row_repr += str( empty_count )
            board_repr.append( row_repr )

        fen_repr = '/'.join( board_repr )
        color = 'w' if self.currentTurn.color=='white' else 'b'

        if self.pieceToPlay is None:
            cell = '-'
        else:
            cell = XY2POS( self.pieceToPlay.x, self.pieceToPlay.y )

        return f"{fen_repr} {color} {cell}"
    
    def dump(self):
        # Initialize an 8x8 matrix with dots
        board = [['.' for _ in range(8)] for _ in range(8)]

        # Place pieces on the board
        for piece in self.pieces:
            symbol = ('k' if piece.king else 'c')
            if piece.player.color == 'white': symbol = symbol.upper()
            board[7 - piece.y][piece.x] = symbol  

        # Add row and column labels
        board_with_labels = ['  a b c d e f g h']
        for i, row in enumerate(board):
            row_label = f'{8 - i} ' + ' '.join(row)  # Adjust for 0-indexing and flip y-axis
            board_with_labels.append(row_label)

        return '\n'.join(board_with_labels)