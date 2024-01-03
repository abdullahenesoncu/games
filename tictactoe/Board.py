from .Player import Player

class Board:
    def __init__(self, n, player1, player2):
        """
        Initializes the board with two players.

        Args:
        player1: The first player object.
        player2: The second player object.
        """
        self.n = n
        self.currentTurn = player1  # Set the current turn to player1
        self.players = [player1, player2]  # List of players
        self.board = []
        for row in range(n):
          self.board.append( [None]*n )

    def canMakeMove(self, x, y):
        """
        Checks if a move can be made at the given cell.

        Args:
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.

        Returns:
        bool: True if the move can be made, False otherwise.
        """
        # A move can be made only if the target cell is empty and in board
        return 0<=x<self.n and 0<=y<self.n and self.board[y][x] is None

    def switchTurn(self):
        """
        Toggles the turn to the other player.
        """
        if self.currentTurn == self.players[1]:
            self.currentTurn = self.players[0]
        else:
            self.currentTurn = self.players[1]
        # self.currentTurn = self.players[0] if self.currentTurn == self.players[1] else self.players[1]

    def makeMove(self, x, y):
        """
        Makes a move on the board at the specified position.

        Args:
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.

        Returns:
        bool: True if the move was successful, False otherwise.
        """
        if not self.canMakeMove(x, y):
            return False  # Move cannot be made

        # Record the move and switch turns
        self.board[y][x] = self.currentTurn.color
        self.switchTurn()
        return True

    def gameStatus(self):
        """
        Returns the status of the game

        Returns:
        str: 'X' or 'O' if a player has won, 'draw' if it's a draw, 'ongoing' otherwise.
        """
        # Check for rows
        for row in range( self.n ):
          for column in range( self.n-2 ):
            if ( self.board[row][column] is not None and
                self.board[row][column] == self.board[row][column+1] == self.board[row][column+2] ):
              return self.board[row][column]

        # Check for columns
        for row in range( self.n-2 ):
          for column in range( self.n ):
            if ( self.board[row][column]  is not None and
                self.board[row][column] == self.board[row+1][column] == self.board[row+2][column] ):
              return self.board[row][column]

        # Check for left diagonals
        for row in range( self.n-2 ):
          for column in range( self.n-2 ):
            if ( self.board[row][column] is not None and
                self.board[row][column] == self.board[row+1][column+1] == self.board[row+2][column+2] ):
              return self.board[row][column]

        # Check for right diagonals
        for row in range( 2, self.n ):
          for column in range( self.n-2 ):
            if ( self.board[row][column] is not None and
                self.board[row][column] == self.board[row-1][column+1] == self.board[row-2][column+2] ):
              return self.board[row][column]

        # Check draw condition, if all cells are non-empty
        # if all( [ c is not None for row in self.board for c in row ] ):
        #       return 'draw'
        for row in self.board:
           for c in row:
              if c is None:
                 return 'ongoing'
        return 'draw'

    def boardToString(self):
        """
        Creates a string representation of the current board state.

        Returns:
        str: The board state as a multi-line string.
        """
        res = "" # result
        header = [" "]
        for i in range(self.n): header.append( chr(ord('a')+i) )
        res += ' '.join(header) + '\n'
        for i in range(self.n):
            row = [ str( self.n-i ) ]
            for j in range(self.n):
                c = self.board[i][j]
                if c is not None:
                  row.append( c )
                else:
                  row.append( '.' )
                #row.append( c if c else '.' )
            res += ' '.join(row) + '\n'
            # The join function concatenates elements of an iterable into a string,
            # separated by the string it's called on.
            # For example, if you call ','.join(['a', 'b', 'c']), it will return 'a,b,c',
            # using ',' as the separator between the elements.
        return res

    def boardToFEN(self):
        #    .../.../... x
        # or xox/x../o.. o
        fen = ""
        for row in self.board:
            rowStr = ""
            for c in row:
                if c is not None:
                    rowStr += c
                else:
                    rowStr += '.'
            fen += rowStr + '/'
        fen = fen[:-1]
        # fen = '/'.join([ ''.join([c if c else '.' for c in row]) for row in self.board ])
        return fen + f' {self.currentTurn.color}'

    @classmethod
    def boardFromFEN(cls, fen):
        fields = fen.split()
        if len(fields) != 2:
            raise ValueError("Invalid FEN string")

        player1 = Player('X', 'x')
        player2 = Player('O', 'o')
        board = cls(len( fields[0].split('/') ), player1, player2)
        # fields[0] is like xox/x../o.., fields[0].split('/') is like ["xox", "x..", "o.."]

        for i, row in enumerate( fields[0].split('/') ): # iterate on ["xox", "x..", "o.."]
            for j, c in enumerate( row ): # iterate on "xox"
                if c != '.':
                    board.board[ i ][ j ] = c
                else:
                    board.board[ i ][ j ] = None
            #board.board[ i ] = [ None if c=='.' else c for c in row ]

        board.currentTurn = player1 if fields[1] == 'x' else player2

        return board
