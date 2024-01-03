from .Pawn import Pawn
from .Rook import Rook
from .Knight import Knight
from .Bishop import Bishop
from .Queen import Queen
from .King import King
from .Board import Board
from .Player import Player
from .GameBase import GameBase
from .helpers import XY2POS, POS2XY

import math

knight_positions = [
    [-5, -4, -3, -3, -3, -3, -4, -5],
    [-4, -2,  0,  1,  1,  0, -2, -4],
    [-3,  1,  2,  2.5, 2.5,  2,  1, -3],
    [-3,  1.5, 2.5, 3, 3, 2.5, 1.5, -3],
    [-3,  1,  2.5, 3, 3, 2.5,  1, -3],
    [-3,  1.5, 2,  2.5, 2.5,  2, 1.5, -3],
    [-4, -2,  1,  1.5, 1.5,  1, -2, -4],
    [-5, -4, -3, -3, -3, -3, -4, -5]
]

bishop_positions = [
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1,  0,  0,  0,  0,  0,  0, -1],
    [-1,  0,  0.5, 1,  1, 0.5,  0, -1],
    [-1,  0.5, 0.5, 1, 1, 0.5, 0.5, -1],
    [-1,  0,  1, 1, 1, 1,  0, -1],
    [-1,  1,  1,  1,  1,  1,  1, -1],
    [-1,  0.5, 0,  0,  0,  0, 0.5, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]
]

rook_positions = [
    [0,  0,  0,  0.5, 0.5,  0,  0,  0],
    [-0.5,  0,  0,  0,  0,  0,  0, -0.5],
    [-0.5,  0,  0,  0,  0,  0,  0, -0.5],
    [-0.5,  0,  0,  0,  0,  0,  0, -0.5],
    [-0.5,  0,  0,  0,  0,  0,  0, -0.5],
    [-0.5,  0,  0,  0,  0,  0,  0, -0.5],
    [0.5,  1,  1,  1,  1,  1,  1, 0.5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

queen_positions = [
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
    [-1,  0,  0,  0,  0,  0,  0, -1],
    [-1,  0, 0.5, 0.5, 0.5, 0.5,  0, -1],
    [-0.5,  0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [0,  0,  0.5, 0.5, 0.5, 0.5,  0, -0.5],
    [-1,  0.5, 0.5, 0.5, 0.5, 0.5,  0, -1],
    [-1,  0, 0.5,  0,  0,  0, 0, -1],
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
]

king_positions_opening = [
    [2, 3, 1, 0, 0, 1, 3, 2],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3]
]

king_positions_endgame = [
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [2, 3, 1, 0, 0, 1, 3, 2],
    [3, 4, 2, 1, 1, 2, 4, 3],
    [3, 4, 2, 1, 1, 2, 4, 3]
]

pawn_positions = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
    [0.5, 1, 1, -2, -2, 1, 1, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

piece_values = {Pawn: 1, Knight: 3, Bishop: 3, Rook: 5, Queen: 9, King: 0}
endgame_threshold = 10


class Chess( GameBase ):
    @classmethod
    def getInitialRepr( cls ):
        return 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    
    @classmethod
    def getPossibleMoves( cls, repr ):
        board = Board.boardFromFEN( repr )
        res = []

        if board.isGameOver():
            return res
        
        for X in range(8):
            for Y in range(8):
                if board.getCell( X, Y ) is None:
                    continue
                if board.getCell( X, Y ).player.color != board.currentTurn.color:
                    continue
                for x in range(8):
                    for y in range(8):
                        for additionalInput in [None, 'q', 'n']:
                            if isinstance( board.getCell( X, Y ), Pawn ) and ( y==0 or y==7 ) and additionalInput is None: continue
                            if not (isinstance( board.getCell( X, Y ), Pawn ) and ( y==0 or y==7 )) and additionalInput is not None: continue
                            if board.getCell( X, Y ).canMove( x, y, board ) or board.getCell( X, Y ).canCapture( x, y, board ):
                                pieceX = X
                                pieceY = Y
                                try:
                                    r = board.movePiece( board.getCell( X, Y ), x, y, additionalInput )
                                    assert( r )
                                except:
                                    print(board.wouldBeInCheck( board.getCell(X,Y), x, y ))
                                    print(board.getCell(X,Y))
                                    print( board.boardToString() )
                                    print(board.boardToFEN())
                                    print( f'{XY2POS( pieceX, pieceY )}{XY2POS( x, y )}',  board.getCell( X, Y ).player.color, board.currentTurn.color )
                                    assert(False)
                                res.append( ( board.boardToFEN(), f'{XY2POS( pieceX, pieceY )}{XY2POS( x, y )}{additionalInput or ""}' ) )
                                board = Board.boardFromFEN( repr )
        return res
    
    @classmethod
    def isGameOver( cls, repr ):
        board = Board.boardFromFEN( repr )
        return board.isGameOver()
    
    @classmethod
    def winner( cls, repr ):
        board = Board.boardFromFEN( repr )
        assert( board.isGameOver() )
        if board.isDraw():
            return 0
        if board.currentTurn.color == 'white':
            return 1
        else:
            return -1
    
    @classmethod
    def getScore(cls, repr):
        board = Board.boardFromFEN(repr)
        score = 0
        is_endgame = len(board.pieces) < endgame_threshold

        if board.isDraw():
            return 0
        elif board.isCheckmate( board.currentTurn ):
            return float('-1000') if board.currentTurn.color == 'white' else float('1000')
        elif board.halfMoveClock > 10:
            return 0
        
        for piece in board.pieces:
            positional_value = 0
            if isinstance(piece, Pawn):
                positional_value = pawn_positions[piece.y][piece.x]
            elif isinstance(piece, Knight):
                positional_value = knight_positions[piece.y][piece.x]
            elif isinstance(piece, Bishop):
                positional_value = bishop_positions[piece.y][piece.x]
            elif isinstance(piece, Rook):
                positional_value = rook_positions[piece.y][piece.x]
            elif isinstance(piece, Queen):
                positional_value = queen_positions[piece.y][piece.x]
            elif isinstance(piece, King):
                if is_endgame:
                    positional_value = king_positions_endgame[piece.y][piece.x]
                else:
                    positional_value = king_positions_opening[piece.y][piece.x]
            
            total_value = piece_values[type(piece)] + positional_value
            if piece.player.color == 'white':
                score += total_value
            else:
                score -= total_value

        # Pawn Structure Analysis
        score += cls.analyzePawnStructure(board)

        # King Safety
        score += cls.evaluateKingSafety(board)

        # Control of the Center
        score += cls.evaluateCenterControl(board)

        # Piece Mobility
        #score += cls.evaluatePieceMobility(board)
        
        if board.currentTurn.color == 'white':
            score -= board.fullMoveNumber
        else:
            score += board.fullMoveNumber

        return score

    @classmethod
    def distanceToEnd(cls, boardRepr):
        board = Board.boardFromFEN(boardRepr)

        # Factors influencing the distance to the end of the game
        total_material = sum(piece_values[type(piece)] for piece in board.pieces)
        num_pieces = len(board.pieces)
        is_endgame = num_pieces < endgame_threshold
        king_safety = cls.evaluateKingSafety(board)

        # Calculate a heuristic score for distance to end
        # Note: These values and formula are heuristic. They can be adjusted based on empirical data or further analysis.
        material_factor = 1 - (total_material / 39)  # 39 is the total material value at the start of the game
        piece_factor = 1 - (num_pieces / 32)  # 32 is the total number of pieces at the start
        endgame_factor = 1 if is_endgame else 0
        king_safety_factor = 1 if king_safety < -5 else 0  # Arbitrary threshold for king safety

        # Combine factors (weights can be adjusted)
        distance_score = (material_factor + piece_factor + endgame_factor + king_safety_factor) / 4

        return 1 - distance_score

    @classmethod
    def analyzePawnStructure(cls, board):
        pawn_structure_score = 0

        # Track positions of pawns for both colors
        white_pawns = set()
        black_pawns = set()

        for piece in board.pieces:
            if isinstance(piece, Pawn):
                if piece.player.color == 'white':
                    white_pawns.add((piece.x, piece.y))
                else:
                    black_pawns.add((piece.x, piece.y))

        # Analyze pawn structure for both colors
        for x in range(8):
            white_pawns_in_file = [y for (px, y) in white_pawns if px == x]
            black_pawns_in_file = [y for (px, y) in black_pawns if px == x]

            # Check for doubled pawns
            if len(white_pawns_in_file) > 1:
                pawn_structure_score -= len(white_pawns_in_file) - 1
            if len(black_pawns_in_file) > 1:
                pawn_structure_score += len(black_pawns_in_file) - 1

            # Check for isolated pawns
            if not any((x-1, y) in white_pawns or (x+1, y) in white_pawns for y in white_pawns_in_file):
                pawn_structure_score -= 1
            if not any((x-1, y) in black_pawns or (x+1, y) in black_pawns for y in black_pawns_in_file):
                pawn_structure_score += 1

            # Check for passed pawns
            if all(y > max(black_pawns_in_file + [-1]) for y in white_pawns_in_file):
                pawn_structure_score += len(white_pawns_in_file)
            if all(y < min(white_pawns_in_file + [8]) for y in black_pawns_in_file):
                pawn_structure_score -= len(black_pawns_in_file)

        # Add more detailed analysis for pawn chains, etc., if needed

        return pawn_structure_score

    @classmethod
    def evaluateKingSafety(cls, board):
        king_safety_score = 0

        # Define a function to assess the safety around the king
        def assess_king_safety(king, opponent_pieces):
            safety_score = 0

            # Check the pawn shield
            for dx in [-1, 0, 1]:
                if board.getCell(king.x + dx, king.y + ( 1 if king.player.color=='white' else -1 )) is None:
                    safety_score -= 1  # Penalize for each open square in front of the king

            # Check for open lines towards the king
            for piece in opponent_pieces:
                if isinstance(piece, (Rook, Queen)) and piece.x == king.x:
                    safety_score -= 2
                if isinstance(piece, (Bishop, Queen)) and abs(piece.x - king.x) == abs(piece.y - king.y):
                    safety_score -= 2

            # Adjust the score based on the king's position (central squares are more dangerous)
            if king.x in [2, 3, 4, 5] and king.y in [2, 3, 4, 5]:
                safety_score -= 2

            return safety_score

        for player in board.players:
            king = next((piece for piece in player.pieces if isinstance(piece, King)), None)
            if king:
                opponent = board.players[1] if player == board.players[0] else board.players[0]
                opponent_pieces = [piece for piece in opponent.pieces if not isinstance(piece, King)]

                # Adjust the score based on the king's safety
                if player.color == 'white':
                    king_safety_score += assess_king_safety(king, opponent_pieces)
                else:
                    king_safety_score -= assess_king_safety(king, opponent_pieces)

        return king_safety_score

    @classmethod
    def evaluateCenterControl(cls, board):
        center_control_score = 0
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]  # d4, e4, d5, e5

        for square in center_squares:
            controlled_by_white = cls.isControlledBy(square, board, 'white')
            controlled_by_black = cls.isControlledBy(square, board, 'black')

            if controlled_by_white and not controlled_by_black:
                center_control_score += 1
            elif controlled_by_black and not controlled_by_white:
                center_control_score -= 1

        return center_control_score

    @classmethod
    def isControlledBy(cls, square, board, color):
        x, y = square
        for piece in board.pieces:
            if piece.player.color == color and piece.canMove(x, y, board):
                return True
        return False

    @classmethod
    def evaluatePieceMobility(cls, board):
        mobility_score = 0

        def count_legal_moves(piece, board):
            legal_moves = 0
            for x in range(8):
                for y in range(8):
                    if piece.canMove(x, y, board) or piece.canCapture(x, y, board):
                        if not board.wouldBeInCheck(piece, x, y):
                            legal_moves += 1
            return legal_moves

        for piece in board.pieces:
            moves = count_legal_moves(piece, board)
            if piece.player.color == 'white':
                mobility_score += moves
            else:
                mobility_score -= moves

        return mobility_score
    
    def __init__( self, player1, player2 ):
        self.player1 = Player(player1, 'white')
        self.player2 = Player(player2, 'black')
        self.board = Board( player1, player2 ).boardFromFEN( self.getInitialRepr() )
    
    def parseInput( self, moveInput ):
        if 4 <= len(moveInput) <= 5:
            return moveInput[ :2 ], moveInput[ 2:4 ], moveInput[ 4: ]
        else:
            return None
    
    def getInput(self):
        moveInput = None
        while moveInput is None:
            moveInput = self.parseInput( input( 'Please Enter Your Move: ' ) )
        return moveInput
    
    def play( self, input ):
        print(input)
        input = self.parseInput(input)
        status = self.board.play(*input)
        assert( status )

    def run(self):
        while not self.board.isGameOver():
            print( self.board.boardToString() )
            moveInput = self.getInput()
            status = self.board.play(*moveInput)
            if status == True:
                print("Move successful.")
            else:
                print("Invalid move. Try again.")
        if self.board.isDraw():
            print( 'Draw!' )
        elif self.board.isCheckmate(self.player1):
            print( f'{self.player2.name} win!' )
        else:
            print( f'{self.player1.name} win!' )

if __name__ == '__main__':
    Chess('Alice', 'Bob').run()
