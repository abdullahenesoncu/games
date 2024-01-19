from .GameBase import GameBase
from .Board import Board
from .Player import Player

valid_inputs = ['a1', 'b1', 'c1', 'a2', 'b2', 'c2', 'a3', 'b3', 'c3']

class TicTacToe ( GameBase ):
    def __init__(self, n, player1, player2):
        """
        Initializes a TicTacToe game with two players.

        Args:
        player1 (str): The name of player 1.
        player2 (str): The name of player 2.
        """
        self.n = n
        self.player1 = Player(player1, "x")
        self.player2 = Player(player2, "o")
        self.board = Board(n, self.player1, self.player2)

    @classmethod
    def getInitialRepr( cls, n=3 ):
        # like '.../.../... x'
        return '/'.join( ['.'*n]*n ) + ' x'

    @classmethod
    def isGameOver(cls, repr):
        return Board.boardFromFEN(repr).gameStatus() in ['o', 'x', 'draw']

    @classmethod
    def winner(cls, repr):
        s = Board.boardFromFEN(repr).gameStatus()
        return 1 if s == 'x' else (-1 if s == 'o' else 0)

    @classmethod
    def getScore(cls, repr):
        board = Board.boardFromFEN(repr)
        gameStatus = board.gameStatus()

        if gameStatus == board.players[0].color:
            return 1
        elif gameStatus == board.players[1].color:
            return -1
        elif gameStatus == 'draw':
            return 0

        return 0

    @classmethod
    def getPossibleMoves(cls, repr):
        board = Board.boardFromFEN(repr)
        possible_moves = []

        for i in range(board.n):
            for j in range(board.n):
                if board.canMakeMove(i, j):
                    board.makeMove(i, j)
                    possible_moves.append((board.boardToFEN(), f'{chr(ord("a")+i)}{3-j}'))
                    board = Board.boardFromFEN(repr)
    
        return possible_moves

    def play( self, input ):
        input = self.parseInput(input)
        status = self.board.makeMove(*input)
        assert( status )

    def getInput(self):
        """
        Gets and validates input from the user until a valid move is entered.

        Returns:
        tuple: The validated move (row, column).
        """
        moveInput = None
        # Loop until a valid move is entered
        while moveInput is None:
            moveInput = self.parseInput(input(f'Please Enter Your Move (like a1, c2) ({self.board.currentTurn.name}): '))
        return moveInput

    def parseInput(self, moveInput):
        """
        Parses and validates the user input.

        Args:
        moveInput (str): The raw input string from the user.

        Returns:
        tuple: The parsed move (row, column) or None if invalid.
        """
        if len(moveInput) == 2 and 0<=ord(moveInput[0])-ord('a')<self.n and 0<int(moveInput[1])<=self.n:
            return ord(moveInput[0])-ord('a'), self.n - int(moveInput[1])
        return None

    def run(self):
        """
        Runs the main game loop.
        """
        # Loop until the game is over
        while True:
            print(self.board.boardToString())  # Display the board
            if self.board.gameStatus() != 'ongoing': break

            moveInput = self.getInput()  # Get user input, in format like a1, b3
            status = self.board.makeMove(*moveInput)  # Execute the move
            if status == True:
                print("Move successful.")
            else:
                print("Invalid move. Try again.")

        gameResult = self.board.gameStatus()
        # Display the game result
        if gameResult == self.player1.color:
            print(f'{self.player1.name} wins')
        elif gameResult == self.player2.color:
            print(f'{self.player2.name} wins')
        else:
            print(' Draw! ')