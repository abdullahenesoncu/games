from .helpers import XY2POS, POS2XY
from .Player import Player
from .QirkatPiece import QirkatPiece

class Board:
    def __init__( self, player1, player2 ):
        self.pieces = []
        self.currentTurn = player1
        self.players = [player1, player2]
        self.pieceToPlay = None
        self.rows = 5
        self.columns = 5

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
            if piece.x + gx == x and piece.y + gy == y:
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
                    return False
                return True
        return False
    
    def move( self, piece, x, y ):
        if not self.canMove( piece, x, y ):
            return False
        if ( x-piece.x, y-piece.y ) in piece.getPossibleDirections():
            piece.x = x
            piece.y = y
            self.switchTurn()
            return True
        for ( cx, cy ), ( gx, gy ) in piece.getPossibleCaptures():
            if piece.x + gx == x and piece.y + gy == y:
                self.simulateCapture(piece, piece.x+gx, piece.y+gy, piece.x+cx, piece.y+cy)
                maxCaptures = self.findCapturesFromPosition(piece, piece.x, piece.y)
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
        if ( len( {p.player for p in self.pieces} ) == 2 and
             not any(self.canMove(piece, piece.x + dx, piece.y + dy) for piece in self.pieces for dx, dy in piece.getPossibleDirections()) and
             not any(self.canMove(piece, piece.x + gx, piece.y + gy) for piece in self.pieces for (cx, cy), (gx, gy) in piece.getPossibleCaptures())):
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
    def boardFromFEN( cls, fen ):
        # 'ccccc/ccccc/cc1CC/CCCCC/CCCCC w -'
        repr, color, cell = fen.split()
        player1 = Player( 'White', 'white' )
        player2 = Player( 'Black', 'black' )
        qirkatboard = cls( player1, player2 )
        assert( len( repr.split( '/' ) ) == 5 )
        for y, line in enumerate( repr.split( '/' ) ):
            x = 0
            for c in line:
                if c.isnumeric():
                    x += int(c)
                else:
                    if c == c.lower():
                        qirkatboard.addPiece( QirkatPiece( player2, XY2POS( x, 4-y ) ) )
                    else:
                        qirkatboard.addPiece( QirkatPiece( player1, XY2POS( x, 4-y ) ) )
                    x += 1
        qirkatboard.currentTurn = player1 if color == 'w' else player2
        qirkatboard.pieceToPlay = None if cell == '-' else qirkatboard.getCell( *POS2XY( cell ) )
        return qirkatboard
    
    def boardToFEN(self):
        board_repr = []
        for j in reversed( range( 5 ) ):
            empty_count = 0
            row_repr = ''
            for i in range( 5 ):
                piece = self.getCell( i, j )
                if not piece:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_repr += str( empty_count )
                        empty_count = 0
                    if piece.player.color == 'white':
                        row_repr += 'C'
                    else:
                        row_repr += 'c'
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
    
    def boardToString(self):
        # Initialize an 5x5 matrix with dots
        board = [['.' for _ in range(5)] for _ in range(5)]

        # Place pieces on the board
        for piece in self.pieces:
            symbol = 'c'
            if piece.player.color == 'white': symbol = symbol.upper()
            board[4 - piece.y][piece.x] = symbol  

        # Add row and column labels
        board_with_labels = ['  a b c d e']
        for i, row in enumerate(board):
            row_label = f'{5 - i} ' + ' '.join(row)  # Adjust for 0-indexing and flip y-axis
            board_with_labels.append(row_label)
        
        board_with_labels.append( f'Player {self.currentTurn.name}\'s turn.' )
        if self.pieceToPlay:
            board_with_labels.append( f'You must play piece at {XY2POS(self.pieceToPlay.x, self.pieceToPlay.y)}' )

        return '\n'.join(board_with_labels)