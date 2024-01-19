from .GameBase import GameBase
from .Board import Board
from .Player import Player
import random

class RoyalGameOfUr(GameBase):
    def __init__(self, player1, player2):
        self.player1 = Player(player1, "x")
        self.player2 = Player(player2, "o")
        self.board = Board(self.player1, self.player2)
    
    @classmethod
    def getInitialRepr(self):
        return "empty 7 empty 7 x"

    @classmethod
    def isGameOver(cls, repr):
        board = Board.boardFromFEN(repr)
        return board.isGameOver()
    
    @classmethod
    def winner(cls, repr):
        board = Board.boardFromFEN(repr)
        return board.winner()

    @classmethod
    def getScore(cls, repr):
        board = Board.boardFromFEN(repr)
        score = 0

        # Points for pieces finished
        score += board.players[0].finishPieces * 1
        score -= board.players[1].finishPieces * 1

        # Additional points for strategic positions (e.g., rosettes: b5, a2, c2)
        strategic_positions = ['b5', 'a2', 'c2', 'a8', 'c8']
        for pos in strategic_positions:
            if pos in board.piecesOnBoard:
                if board.piecesOnBoard[pos] == board.players[0]:
                    score += 0.5  # Half a point for each piece on a strategic position
                else:
                    score -= 0.5

        # Subtract points for pieces still at start
        score -= board.players[0].startPieces * 0.25
        score += board.players[1].startPieces * 0.25

        return score

    @classmethod
    def getPossibleMoves(cls, repr, dice):
        moves = []
        board = Board.boardFromFEN(repr)
        if board.currentTurn.startPieces and board.canMove('st', dice):
            board.move('st', dice)
            moves.append( (board.boardToFEN(), 'st') )
            board = Board.boardFromFEN(repr)
        for pos in list( board.piecesOnBoard.keys() ):
            if board.canMove(pos, dice):
                board.move(pos, dice)
                moves.append( (board.boardToFEN(), pos) )
                board = Board.boardFromFEN(repr)
        return moves
    
    @classmethod
    def diceStates(cls):
        return [ (0, 1/16), (1, 4/16), (2, 6/16), (3, 4/16), (4, 1/16) ]
    
    @classmethod
    def rollDice(cls):
        x = random.randint(0, 15)
        if x < 1:
            return 0
        if x < 5:
            return 1
        if x < 11:
            return 2
        if x < 15:
            return 3
        return 4
    
    @classmethod
    def hasDice(cls):
        return True

    def play(self, input, dice):
        if not dice or not self.board.hasCurrentPlayerMove(dice):
            return True
        return self.board.move(input, dice)

    def getInput(self):
        moveInput = input(f'Please Enter Your Move ({self.board.currentTurn.name}) (st, fn, a1, c2, ...): ')
        return moveInput

    def parseInput(self, moveInput):
        if len(moveInput) != 2:
            return None
        return moveInput

    def run(self):
        while not self.board.isGameOver():
            print(self.board.boardToString())
            dice = self.rollDice()
            print("Dice: ", dice)
            if not dice or not self.board.hasCurrentPlayerMove(dice):
                print("Don't move")
                continue
            moveInput = self.getInput()
            parsedInput = self.parseInput(moveInput)
            if parsedInput:
                if not self.play(parsedInput, dice):
                    print("Invalid move. Try again.")
            else:
                print("Invalid move. Try again.")

        winner = self.winner()
        if winner:
            print(f'{winner} wins!')
        else:
            print('Draw!')