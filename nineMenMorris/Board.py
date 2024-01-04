from .Player import Player
from .helpers import POS2XY, XY2POS

adjacency_list = {
    'a1': ['d1', 'a4'],
    'd1': ['a1', 'g1', 'd2'],
    'g1': ['d1', 'g4'],
    'b2': ['d2', 'b4'],
    'd2': ['b2', 'f2', 'd1', 'd3'],
    'f2': ['d2', 'f4'],
    'c3': ['d3', 'c4'],
    'd3': ['c3', 'e3', 'd2'],
    'e3': ['d3', 'e4'],
    'a4': ['a1', 'a7', 'b4'],
    'b4': ['a4', 'b2', 'b6', 'c4'],
    'c4': ['b4', 'c3', 'c5'],
    'e4': ['e3', 'e5', 'f4'],
    'f4': ['e4', 'f2', 'f6', 'g4'],
    'g4': ['f4', 'g1', 'g7'],
    'c5': ['c4', 'd5'],
    'd5': ['c5', 'e5', 'd6'],
    'e5': ['d5', 'e4'],
    'b6': ['b4', 'd6'],
    'd6': ['b6', 'f6', 'd5', 'd7'],
    'f6': ['d6', 'f4'],
    'a7': ['a4', 'd7'],
    'd7': ['a7', 'g7', 'd6'],
    'g7': ['d7', 'g4']
}

mill_possibilities = [
    # Horizontal mills on each row
    ('a1', 'd1', 'g1'),
    ('b2', 'd2', 'f2'),
    ('c3', 'd3', 'e3'),
    ('a4', 'b4', 'c4'),
    ('e4', 'f4', 'g4'),
    ('c5', 'd5', 'e5'),
    ('b6', 'd6', 'f6'),
    ('a7', 'd7', 'g7'),
    # Vertical mills on each column
    ('a1', 'a4', 'a7'),
    ('b2', 'b4', 'b6'),
    ('c3', 'c4', 'c5'),
    ('d1', 'd2', 'd3'), # vertical middle
    ('d5', 'd6', 'd7'), # vertical middle
    ('e3', 'e4', 'e5'),
    ('f2', 'f4', 'f6'),
    ('g1', 'g4', 'g7')
]

PLACING_PHASE = 'placing_phase'
MOVING_PHASE = 'moving_phase'
FLYING_PHASE = 'flying_phase'
GAME_OVER = 'game_over'

class Board:
    def __init__(self, player1, player2):
        self.currentTurn = player1  # Set the current turn to player1
        self.players = [player1, player2]  # List of players
        self.board = []
        for row in range(7):
          self.board.append( [None]*7 )

    def isConnected(self, pos1, pos2):
        """
        Checks if there is a direct line between two positions on the board.

        Args:
            pos1 (str): The first position (e.g., 'a5').
            pos2 (str): The second position (e.g., 'b3').

        Returns:
            bool: True if there is a direct line, False otherwise.
        """
        # Check if pos2 is in the list of connections for pos1
        return pos2 in self.adjacency_list.get(pos1, [])
    
    def isValidPosition(self, pos):
        """
        Checks if a given position is valid on the Nine Men's Morris board.

        Args:
            pos (str): The position to check (e.g., 'a5').

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        # A position is valid if it exists in the adjacency list
        return pos in adjacency_list
    
    def getCell(self, pos):
        assert( self.isValidPosition(pos) )
        x, y = POS2XY(pos)
        return self.board[x][y]
    
    def setCell(self, pos, value):
        assert( self.isValidPosition(pos) )
        x, y = POS2XY(pos)
        self.board[x][y] = value

    def isInMill(self, pos):
        cell = self.getCell(pos)

        for millPos in mill_possibilities:
            if pos not in millPos: continue
            if all( [ self.getCell(piecePos)==cell for piecePos in millPos] ):
                return True, millPos
        
        return False
    
    def getPiecesOfPlayer(self, player):
        res = []
        for pos in adjacency_list:
            c = self.getCell(pos)
            if c == player.color:
                res.append(pos)
        return res

    def removablePiecesOfPlayer(self, player):
        piecesOfPlayer = self.getPiecesOfPlayer(player)
        isInMill = [self.isInMill(pos) for pos in piecesOfPlayer] 
        if all( isInMill ):
            return piecesOfPlayer
        return [p for i, p in enumerate(piecesOfPlayer) if not isInMill[i]]
    
    def switchTurn(self):
        self.currentTurn = self.players[0] if self.currentTurn == self.players[1] else self.players[1]
    
    def getPhaseOfPlayer(self, player):
        if player.outBoardPieces > 0:
            return PLACING_PHASE
        piecesOfPlayer = self.getPiecesOfPlayer(player)
        if len( piecesOfPlayer ) < 3:
            return GAME_OVER
        if len( self.getPiecesOfPlayer(player) ) == 3:
            return FLYING_PHASE
        return MOVING_PHASE
    
    def canMovePlacingPhase(self, input):
        if len(input) not in [2, 4]:
            return False
        placePos = input[:2]
        if self.getCell(placePos) is not None:
            return False
        self.setCell(placePos, self.currentTurn.color)
        if len(input) == 4:
            if not self.isInMill(placePos):
                self.setCell(placePos, None)
                return False
            removePos = input[4:]
            removablePieces = self.removablePiecesOfPlayer(self.getOpponent(self.currentTurn))
            if removePos not in removablePieces:
                self.setCell(placePos, None)
                return False
        self.setCell(placePos, None)
        return True
    
    def canMoveMovingPhase(self, input):
        if len(input) not in [4, 6]:
            return False
        fromPos = input[:2]
        toPos = input[2:4]
        fromCell = self.getCell(fromPos)
        toCell = self.getCell(toPos)
        if fromCell != self.currentTurn.color or toCell is not None:
            return False
        if toPos not in adjacency_list[fromPos]:
            return False
        self.setCell(fromPos, None)
        self.setCell(toPos, self.currentTurn.color)
        if len(input) == 6:
            if not self.isInMill(toPos):
                self.setCell(fromPos, self.currentTurn.color)
                self.setCell(toPos, None)
                return False
            removePos = input[4:]
            removablePieces = self.removablePiecesOfPlayer(self.getOpponent(self.currentTurn))
            if removePos not in removablePieces:
                self.setCell(fromPos, self.currentTurn.color)
                self.setCell(toPos, None)
                return False
        self.setCell(fromPos, self.currentTurn.color)
        self.setCell(toPos, None)
        return True
        
    def canMoveFlyingPhase(self, input):
        if len(input) not in [4, 6]:
            return False
        fromPos = input[:2]
        toPos = input[2:4]
        fromCell = self.getCell(fromPos)
        toCell = self.getCell(toPos)
        if fromCell != self.currentTurn.color or toCell is not None:
            return False
        self.setCell(fromPos, None)
        self.setCell(toPos, self.currentTurn.color)
        if len(input) == 6:
            if not self.isInMill(toPos):
                self.setCell(fromPos, self.currentTurn.color)
                self.setCell(toPos, None)
                return False
            removePos = input[4:]
            removeCell = self.getCell(removePos)
            if removeCell is None or removeCell == self.currentTurn.color:
                self.setCell(fromPos, self.currentTurn.color)
                self.setCell(toPos, None)
                return False
        self.setCell(fromPos, self.currentTurn.color)
        self.setCell(toPos, None)
        return True
        
    def canMove(self, input):
        phase = self.getPhaseOfPlayer(self.currentTurn)
        if phase == PLACING_PHASE:
            return self.canMovePlacingPhase(input)
        elif phase == MOVING_PHASE:
            return self.canMoveMovingPhase(input)
        elif phase == FLYING_PHASE:
            return self.canMoveFlyingPhase(input)
        return False

    def move(self, input):
        if self.canMove(input):
            if self.getPhaseOfPlayer(self.currentTurn) == PLACING_PHASE:
                self.movePlacingPhase(input)
            elif self.getPhaseOfPlayer(self.currentTurn) == MOVING_PHASE:
                self.moveMovingPhase(input)
            elif self.getPhaseOfPlayer(self.currentTurn) == FLYING_PHASE:
                self.moveFlyingPhase(input)
            self.switchTurn()
            return True
        return False

    def movePlacingPhase(self, input):
        placePos = input[:2]
        self.setCell(placePos, self.currentTurn.color)
        if len(input) == 4:
            removePos = input[2:]
            self.setCell(removePos, None)
        self.currentTurn.outBoardPieces -= 1

    def moveMovingPhase(self, input):
        fromPos = input[:2]
        toPos = input[2:4]
        self.setCell(fromPos, None)
        self.setCell(toPos, self.currentTurn.color)
        if len(input) == 6:
            removePos = input[4:]
            self.setCell(removePos, None)

    def moveFlyingPhase(self, input):
        fromPos = input[:2]
        toPos = input[2:4]
        self.setCell(fromPos, None)
        self.setCell(toPos, self.currentTurn.color)
        if len(input) == 6:
            removePos = input[4:]
            self.setCell(removePos, None)
            
    def getOpponent(self, player):
        return self.players[1] if player == self.players[0] else self.players[0]
    
    def hasMove(self, player):
        if self.getPhaseOfPlayer(player) == FLYING_PHASE:
            return True
        if self.getPhaseOfPlayer(player) == PLACING_PHASE:
            return True

        for pos in self.getPiecesOfPlayer(player):
            for adjacent in adjacency_list[pos]:
                if self.getCell(adjacent) is None:
                    return True
        return False
    
    def boardToString(self):
        # Define the empty board representation
        board_lines = [
            "O - - O - - O",
            "| O - O - O |",
            "| | O O O | |",
            "O O O   O O O",
            "| | O O O | |",
            "| O - O - O |",
            "O - - O - - O"
        ]
        
        # Update the board representation with the current pieces
        for pos in adjacency_list:
            x, y = POS2XY(pos)
            piece = self.getCell(pos)
            if piece:  # If there is a piece, replace the corresponding character
                line = list(board_lines[6 - y])  # Convert row index because we count from bottom
                line[2 * x] = piece  # Multiply by 2 because of the dots
                board_lines[6 - y] = "".join(line)
        
        # Add row numbers and column letters
        board_with_labels = ["  a b c d e f g"]
        for i, line in enumerate(board_lines, 1):  # Start from 1, reverse the lines
            board_with_labels.append(f"{8-i} {line}")
        
        board_with_labels.append(f'Outboard pieces of {self.currentTurn.name} is {self.currentTurn.outBoardPieces}')
        board_with_labels.append(f'Inboard pieces of {self.currentTurn.name} is {len(self.getPiecesOfPlayer(self.currentTurn))}')
        board_with_labels.append(f'Phase {self.getPhaseOfPlayer(self.currentTurn)}')
        
        # Join all the lines into a single string
        return "\n".join(board_with_labels)
    
    def boardToFEN(self):
        fen = ''
        for pos in adjacency_list:
            piece = self.getCell(pos)
            fen += piece if piece else 'O'
        fen += ' ' + ('w' if self.currentTurn == self.players[0] else 'b') + ' ' + str(self.players[0].outBoardPieces) + ' ' + str(self.players[1].outBoardPieces)
        return fen

    @classmethod
    def boardFromFEN(cls, fen):
        board_state, currentTurn, o1, o2 = fen.split()
        player1 = Player('W', 'w')
        player2 = Player('B', 'b')
        player1.outBoardPieces = int(o1)
        player2.outBoardPieces = int(o2)
        board = cls(player1, player2)
        board.currentTurn = player1 if currentTurn == 'w' else player2

        for pos, piece in zip(adjacency_list, board_state):
            if piece != 'O':
                board.setCell(pos, piece)
        
        return board