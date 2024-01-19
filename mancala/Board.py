from .Player import Player

class MancalaBoard:
    def __init__(self, player1, player2):
        """
        Initializes the Mancala board with two players.

        Args:
        player1: The first player object.
        player2: The second player object.
        """
        self.players = [player1, player2]
        self.currentTurn = player1
        self.board = [4]*12  # 6 pits for each player, each starting with 4 seeds
        self.stores = [0, 0]  # Two stores, one for each player

    def canMakeMove(self, pit):
        """
        Checks if a move can be made from the given pit.

        Args:
        pit (int): The index of the pit.

        Returns:
        bool: True if the move can be made, False otherwise.
        """
        return self.board[pit] > 0 and self.isCurrentPlayerPit(pit)

    def isCurrentPlayerPit(self, pit):
        """
        Checks if the pit belongs to the current player.

        Args:
        pit (int): The index of the pit.

        Returns:
        bool: True if the pit belongs to the current player, False otherwise.
        """
        playerIndex = self.players.index(self.currentTurn)
        return (playerIndex * 6) <= pit < ((playerIndex + 1) * 6)

    def makeMove(self, pit):
        """
        Makes a move from the specified pit.

        Args:
        pit (int): The index of the pit.

        Returns:
        bool: True if the move was successful, False otherwise.
        """
        if not self.canMakeMove(pit):
            return False

        # Sowing seeds
        seeds = self.board[pit]
        self.board[pit] = 0
        currentIndex = pit

        while seeds > 0:
            currentIndex = (currentIndex + 1) % 12
            if currentIndex != pit:  # Skip the original pit
                self.board[currentIndex] += 1
                seeds -= 1

        # Capture condition
        if self.board[currentIndex] == 1 and self.isCurrentPlayerPit(currentIndex):
            oppositePit = 11 - currentIndex
            self.stores[self.players.index(self.currentTurn)] += 1 + self.board[oppositePit]
            self.board[currentIndex] = self.board[oppositePit] = 0

        self.switchTurn()
        return True

    def switchTurn(self):
        """
        Toggles the turn to the other player.
        """
        self.currentTurn = self.players[0] if self.currentTurn == self.players[1] else self.players[1]

    def gameStatus(self):
        """
        Returns the status of the game.

        Returns:
        str: 'Player1' or 'Player2' if a player has won, 'draw' if it's a draw, 'ongoing' otherwise.
        """
        if all(seeds == 0 for seeds in self.board[:6]) or all(seeds == 0 for seeds in self.board[6:]):
            if self.stores[0] > self.stores[1]:
                return 'Player1'
            elif self.stores[1] > self.stores[0]:
                return 'Player2'
            else:
                return 'draw'
        return 'ongoing'

    def boardToString(self):
        """
        Creates a string representation of the current board state.

        Returns:
        str: The board state as a string.
        """
        top_row = self.board[6:12][::-1]  # Player 2's pits
        bottom_row = self.board[0:6]      # Player 1's pits
        top_row_str = ' '.join(str(seeds) for seeds in top_row)
        bottom_row_str = ' '.join(str(seeds) for seeds in bottom_row)
        return f"Player2 Store: {self.stores[1]}\n{top_row_str}\n{bottom_row_str}\nPlayer1 Store: {self.stores[0]}"

    def isGameOver(self):
        """
        Checks if the game is over.

        Returns:
        bool: True if the game is over, False otherwise.
        """
        return all(seeds == 0 for seeds in self.board[:6]) or all(seeds == 0 for seeds in self.board[6:])

    def collectRemainingSeeds(self):
        """
        At the end of the game, collects all remaining seeds to the respective stores.
        """
        if all(seeds == 0 for seeds in self.board[:6]):
            self.stores[1] += sum(self.board[6:12])
            self.board[6:12] = [0] * 6
        elif all(seeds == 0 for seeds in self.board[6:]):
            self.stores[0] += sum(self.board[:6])
            self.board[:6] = [0] * 6
    
def choosePit(player):
    """
    Asks the player to choose a pit to play from.

    Returns:
    int: The chosen pit index.
    """
    pit = int(input(f"{player.name}, choose your pit (1-6): ")) - 1
    return pit

def play_mancala():
    player1 = Player('Player1', 'white')
    player2 = Player('Player2', 'black')
    board = MancalaBoard(player1, player2)

    while not board.isGameOver():
        print(board.boardToString())
        current_player = board.currentTurn
        pit = choosePit(current_player)

        # Check if chosen pit is valid
        while not board.canMakeMove(pit):
            print("Invalid move. Try again.")
            pit = choosePit(current_player)

        board.makeMove(pit)

        # Check if game is over and collect remaining seeds
        if board.isGameOver():
            board.collectRemainingSeeds()
            print("Game Over!")
            print(board.boardToString())
            print(f"Winner: {board.gameStatus()}")
            break

play_mancala()
