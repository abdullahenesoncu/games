from .Player import Player
from .helpers import POS2XY, XY2POS

paths = [
    ["st", "a5", "a6", "a7", "a8", "b8", "b7", "b6", "b5", "b4", "b3", "b2", "b1", "a1", "a2", "fn"],
    ["st", "c5", "c6", "c7", "c8", "b8", "b7", "b6", "b5", "b4", "b3", "b2", "b1", "c1", "c2", "fn"],
]

class Board:
    def __init__(self, player1, player2):
        self.currentTurn = player1  # Set the current turn to player1
        self.players = [player1, player2]  # List of players
        self.paths = {
            player1: paths[0],
            player2: paths[1],
        }
        self.piecesOnBoard = {}
    
    def getNextCell(self, pos, dice, player):
        try:
            index = self.paths[player].index(pos)
        except:
            return None
        newIndex = index + dice
        if newIndex >= len(self.paths[player]):
            return None
        return self.paths[player][newIndex]
    
    def canMove(self, pos, dice):
        if pos == 'a4' or pos == 'c4':
            if self.currentTurn.startPieces == 0:
                return False
            nextPos = self.getNextCell(pos, dice, self.currentTurn)
            if nextPos in self.piecesOnBoard:
                return False
            return True

        if pos not in self.piecesOnBoard:
            return False
        if self.piecesOnBoard[pos] != self.currentTurn:
            return False

        nextPos = self.getNextCell(pos, dice, self.currentTurn)
        if nextPos is None:
            return False
        if nextPos in self.piecesOnBoard:
            if self.piecesOnBoard[nextPos] == self.currentTurn:
                return False
            if nextPos == 'b5':
                return False
        return True
    
    def move(self, pos, dice):
        # Check if the move is valid
        if not self.canMove(pos, dice):
            return False  # Invalid move

        nextPos = self.getNextCell(pos, dice, self.currentTurn)

        # Handle piece movement and capture
        if pos in self.piecesOnBoard:
            del self.piecesOnBoard[pos]  # Remove piece from current position
        if nextPos in self.piecesOnBoard:
            opponent = self.oponentOfPlayer(self.currentTurn)
            opponent.startPieces += 1
            del self.piecesOnBoard[nextPos]

        # Place piece in the new position if it's still on the board
        if nextPos != 'fn':
            self.piecesOnBoard[nextPos] = self.currentTurn
        else:
            self.currentTurn.finishPieces += 1

        if nextPos not in [ 'a8', 'c8', 'b5', 'a2', 'c2' ]:
            self.switchTurn()

        return True

    def isGameOver(self):
        if self.players[0].finishPieces == 7 or self.players[1].finishPieces == 7:
            return True
        return False

    def winner(self):
        if self.players[0].finishPieces == 7:
            return 1
        if self.players[1].finishPieces == 7:
            return -1
        return 0
    
    def hasCurrentPlayerMove(self, dice):
        if self.currentTurn.startPieces and self.canMove('st', dice):
            return True
        for pos, player in self.piecesOnBoard.items():
            if player == self.currentTurn and self.canMove(pos, dice):
                return True
        return False

    def oponentOfPlayer(self, player):
        self.players[0] if self.currentTurn == self.players[1] else self.players[1]

    def switchTurn(self):
        self.currentTurn = self.oponentOfPlayer( self.currentTurn )
    
    def boardToString(self):
        # Define the empty board representation
        board_lines =  ['  a b c',
                        '8 * . *',
                        '7 . . .',
                        '6 . . .',
                        '5 . * .',
                        '4   .  ',
                        '3   .  ',
                        '2 * . *',
                        '1 . . .',
                        ]
        
        # Update the board representation with the current pieces
        for pos, player in self.piecesOnBoard.items():
            r = 9 - int( pos[1] )
            c = ( ord(pos[0])-ord('a') ) * 2 + 2
            if player == self.players[0]:
                board_lines[r][c] = 'X'
            else:
                board_lines[r][c] = 'O'
        
        board_lines.append(
             '  st fn\n'\
            f'X {self.players[0].startPieces} {self.players[0].finishPieces}\n'
            f'O {self.players[1].startPieces} {self.players[1].finishPieces}\n'
        )
        
        # Join all the lines into a single string
        return "\n".join(board_lines)
    
    def boardToFen(self):
        xPieces = []
        oPieces = []
        for pos, player in self.piecesOnBoard:
            if player == self.players[0]:
                xPieces.append(pos)
            else:
                oPieces.append(pos)
        xPieces = ','.join(xPieces)
        yPieces = ','.join(yPieces)
        return f'{xPieces} {self.players[0].startPieces} {yPieces} {self.players[1].startPieces} {"x" if self.currentTurn==self.players[0] else "o"}'
    
    @classmethod
    def boardFromFEN(cls, fen):
        player1 = Player('W', 'w')
        player2 = Player('B', 'b')
        xPieces, xStartPieces, yPieces, yStartPieces, currentTurn = fen.split()
        xPieces = xPieces.split(',')
        yPieces = yPieces.split(',')
        player1.startPieces = int(xStartPieces)
        player2.startPieces = int(yStartPieces)
        player1.finishPieces = 7 - player1.startPieces - len(xPieces)
        player2.finishPieces = 7 - player2.startPieces - len(yPieces)
        board = cls(player1, player2)
        for pos in xPieces:
            board.piecesOnBoard[pos] = player1
        for pos in yPieces:
            board.piecesOnBoard[pos] = player2
        board.currentTurn = player1 if currentTurn == 'x' else player2
        return board