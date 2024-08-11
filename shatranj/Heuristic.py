from .Piyade import Piyade
from .Rook import Rook
from .Horse import Horse
from .Fil import Fil
from .Vizier import Vizier
from .Shah import Shah
from .Board import Board

horse_positions = [
    [-5, -4, -3, -3, -3, -3, -4, -5],
    [-4, -2,  0,  1,  1,  0, -2, -4],
    [-3,  1,  2,  2.5, 2.5,  2,  1, -3],
    [-3,  1.5, 2.5, 3, 3, 2.5, 1.5, -3],
    [-3,  1,  2.5, 3, 3, 2.5,  1, -3],
    [-3,  1.5, 2,  2.5, 2.5,  2, 1.5, -3],
    [-4, -2,  1,  1.5, 1.5,  1, -2, -4],
    [-5, -4, -3, -3, -3, -3, -4, -5]
]

Fil_positions = [
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

vizier_positions = [
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
    [-1,  0,  0,  0,  0,  0,  0, -1],
    [-1,  0, 0.5, 0.5, 0.5, 0.5,  0, -1],
    [-0.5,  0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [0,  0,  0.5, 0.5, 0.5, 0.5,  0, -0.5],
    [-1,  0.5, 0.5, 0.5, 0.5, 0.5,  0, -1],
    [-1,  0, 0.5,  0,  0,  0, 0, -1],
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
]

shah_positions_opening = [
    [2, 3, 1, 0, 0, 1, 3, 2],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3]
]

shah_positions_endgame = [
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [2, 3, 1, 0, 0, 1, 3, 2],
    [3, 4, 2, 1, 1, 2, 4, 3],
    [3, 4, 2, 1, 1, 2, 4, 3]
]

piyade_positions = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
    [0.5, 1, 1, -2, -2, 1, 1, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

piece_values = {Piyade: 1, Horse: 3, Fil: 2, Rook: 5, Vizier: 2, Shah: 0}

@Board.extension
def getScore(self, soft=False):
    score = 0

    if self.isDraw():
        return 0
    elif self.isCheckmate():
        return float('-1000') if self.currentTurn == self.players[ 0 ] else float('1000')

    if self.isCheck():
        score = float('-200') if self.currentTurn == self.players[ 0 ] else float('200')

    for piece in self.pieces:
        total_value = piece_values[type(piece)]
        if piece.player.color == 'white':
            score += total_value
        else:
            score -= total_value

    if not soft:
        # Piyade Structure Analysis
        score += self.analyzePiyadeStructure()

        # Shah Safety
        score += self.evaluateShahSafety()

        # Control of the Center
        score += self.evaluateCenterControl()

        # Piece Mobility
        # score += cls.evaluatePieceMobility()

    return score

@Board.extension
def analyzePiyadeStructure(self):
    piyade_structure_score = 0

    # Track positions of piyades for both colors
    white_piyades = set()
    black_piyades = set()

    for piece in self.pieces:
        if isinstance(piece, Piyade):
            if piece.player.color == 'white':
                white_piyades.add((piece.x, piece.y))
            else:
                black_piyades.add((piece.x, piece.y))

    # Analyze piyade structure for both colors
    for x in range(8):
        white_piyades_in_file = [y for (px, y) in white_piyades if px == x]
        black_piyades_in_file = [y for (px, y) in black_piyades if px == x]

        # Check for doubled piyades
        if len(white_piyades_in_file) > 1:
            piyade_structure_score -= len(white_piyades_in_file) - 1
        if len(black_piyades_in_file) > 1:
            piyade_structure_score += len(black_piyades_in_file) - 1

        # Check for isolated piyades
        if not any((x-1, y) in white_piyades or (x+1, y) in white_piyades for y in white_piyades_in_file):
            piyade_structure_score -= 1
        if not any((x-1, y) in black_piyades or (x+1, y) in black_piyades for y in black_piyades_in_file):
            piyade_structure_score += 1

        # Check for passed piyades
        if all(y > max(black_piyades_in_file + [-1]) for y in white_piyades_in_file):
            piyade_structure_score += len(white_piyades_in_file)
        if all(y < min(white_piyades_in_file + [8]) for y in black_piyades_in_file):
            piyade_structure_score -= len(black_piyades_in_file)

    return piyade_structure_score

@Board.extension
def evaluateShahSafety(self):
    shah_safety_score = 0

    # Define a function to assess the safety around the shah
    def assess_shah_safety(shah, opponent_pieces):
        safety_score = 0

        # Check the piyade shield
        for dx in [-1, 0, 1]:
            if self.getCell(shah.x + dx, shah.y + ( 1 if shah.player.color=='white' else -1 )) is None:
                safety_score -= 1  # Penalize for each open square in front of the shah

        # Check for open lines towards the shah
        for piece in opponent_pieces:
            if isinstance(piece, (Rook, Vizier)) and piece.x == shah.x:
                safety_score -= 2
            if isinstance(piece, (Fil, Vizier)) and abs(piece.x - shah.x) == abs(piece.y - shah.y):
                safety_score -= 2

        # Adjust the score based on the shah's position (central squares are more dangerous)
        if shah.x in [2, 3, 4, 5] and shah.y in [2, 3, 4, 5]:
            safety_score -= 2

        return safety_score

    for player in self.players:
        shah = next((piece for piece in player.pieces if isinstance(piece, Shah)), None)
        if shah:
            opponent = self.opponent( player )
            opponent_pieces = [piece for piece in opponent.pieces if not isinstance(piece, Shah)]

            # Adjust the score based on the shah's safety
            if player.color == 'white':
                shah_safety_score += assess_shah_safety(shah, opponent_pieces)
            else:
                shah_safety_score -= assess_shah_safety(shah, opponent_pieces)

    return shah_safety_score

@Board.extension
def evaluateCenterControl(self):
    center_control_score = 0
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]  # d4, e4, d5, e5

    for square in center_squares:
        controlled_by_white = self.isControlledBy(square, 'white')
        controlled_by_black = self.isControlledBy(square, 'black')

        if controlled_by_white and not controlled_by_black:
            center_control_score += 1
        elif controlled_by_black and not controlled_by_white:
            center_control_score -= 1

    return center_control_score

@Board.extension
def isControlledBy(self, square, color):
    x, y = square
    for piece in self.pieces:
        if piece.player.color == color and piece.canMove(x, y, self):
            return True
    return False

@classmethod
def evaluatePieceMobility(self):
    mobility_score = 0

    def count_legal_moves(piece):
        legal_moves = 0
        for x in range(8):
            for y in range(8):
                if piece.canMove(x, y, self) or piece.canCapture(x, y, self):
                    if not self.wouldBeInCheck(piece, x, y):
                        legal_moves += 1
        return legal_moves

    for piece in self.pieces:
        moves = count_legal_moves(piece)
        if piece.player.color == 'white':
            mobility_score += moves
        else:
            mobility_score -= moves

    return mobility_score
