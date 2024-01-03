from .GameBase import GameBase
from .Board import Board, adjacency_list, GAME_OVER, FLYING_PHASE, MOVING_PHASE, PLACING_PHASE
from .Player import Player

class NineMenMorris(GameBase):
    def __init__(self, player1, player2):
        self.player1 = Player(player1, "w")
        self.player2 = Player(player2, "b")
        self.board = Board(self.player1, self.player2)
    
    @classmethod
    def getInitialRepr(self):
        return Board(Player('W','w'), Player('B','b')).dumpFEN()

    @classmethod
    def isGameOver(cls, repr):
        board = Board.loadFEN(repr)
        if not board.hasMove(board.currentTurn):
            return True
        return board.getPhaseOfPlayer(board.currentTurn) == GAME_OVER
    
    @classmethod
    def winner(cls, repr):
        board = Board.loadFEN(repr)
        if not board.hasMove(board.currentTurn):
            return -1
        phase = board.getPhaseOfPlayer(board.currentTurn)
        if phase == GAME_OVER:
            if len(board.getPiecesOfPlayer(board.players[0]))<=2:
                return -1
            else:
                return 1
        return 0

    @classmethod
    def getScore(cls, repr):
        if cls.isGameOver(repr):
            return cls.winner(repr) * 300
        board = Board.loadFEN(repr)
        p1 = len(board.getPiecesOfPlayer(board.players[0])) + board.players[0].outBoardPieces
        p2 = len(board.getPiecesOfPlayer(board.players[1])) + board.players[1].outBoardPieces
        return p1 ** 2 - p2 ** 2

    @classmethod
    def getPossibleMoves(cls, repr):
        board = Board.loadFEN(repr)
        moves = []
        phase = board.getPhaseOfPlayer(board.currentTurn)
        player = board.currentTurn
        pieces = board.getPiecesOfPlayer(player)
        oponentPieces = board.getPiecesOfPlayer(board.getOpponent(player))
        if phase == PLACING_PHASE:
            for pos in adjacency_list:
                if pos not in pieces + oponentPieces:
                    board.move(pos)
                    moves.append((board.dumpFEN(), pos))
                    board = Board.loadFEN(repr)
                for capture_pos in oponentPieces:
                    if board.canMove(pos+capture_pos):
                        board.move(pos+capture_pos)
                        moves.append((board.dumpFEN(), pos+capture_pos))
                        board = Board.loadFEN(repr)
        elif phase == MOVING_PHASE or phase == FLYING_PHASE:
            for pos in pieces:
                for next_pos in adjacency_list[pos]:
                    if board.canMove(pos+next_pos):
                        board.move(pos+next_pos)
                        moves.append((board.dumpFEN(), pos+next_pos))
                        board = Board.loadFEN(repr)
                    for capture_pos in oponentPieces:
                        if board.canMove(pos+next_pos+capture_pos):
                            board.move(pos+next_pos+capture_pos)
                            moves.append((board.dumpFEN(), pos+next_pos+capture_pos))
                            board = Board.loadFEN(repr)
        return moves

    def play(self, input):
        status = False
        phase = self.board.getPhaseOfPlayer(self.board.currentTurn)
        if phase == PLACING_PHASE:
            status = self.board.canMovePlacingPhase(input)
        elif phase == MOVING_PHASE:
            status = self.board.canMoveMovingPhase(input)
        elif phase == FLYING_PHASE:
            status = self.board.canMoveFlyingPhase(input)
        if status:
            self.board.move(input)
        return status

    def getInput(self):
        moveInput = input(f'Please Enter Your Move ({self.board.currentTurn.name}): ')
        return moveInput

    def parseInput(self, moveInput):
        if len(moveInput) not in [2, 4, 6]:
            return None
        for i in range(0, len(moveInput), 2):
            if moveInput[i:i+2] not in adjacency_list:
                return None
        return moveInput

    def run(self):
        while not self.isGameOver():
            print(self.board.dump())
            moveInput = self.getInput()
            parsedInput = self.parseInput(moveInput)
            if parsedInput:
                if self.play(parsedInput):
                    self.play(parsedInput)
                else:
                    print("Invalid move. Try again.")
            else:
                print("Invalid move. Try again.")

        winner = self.winner()
        if winner:
            print(f'{winner} wins!')
        else:
            print('Draw!')