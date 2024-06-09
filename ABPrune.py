from tictactoe.Game import TicTacToe
from qirkat.Game import Qirkat
from checker.Game import Checker
from nineMenMorris.Game import NineMenMorris
from royalGameOfUr.Game import RoyalGameOfUr
from shatranj.Game import Shatranj

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def lookup(self, key):
        return self.table.get(key)

    def store(self, key, value):
        self.table[key] = value

class AlphaBetaAI:
    def __init__(self, gameClass, maxDepth=10):
        self.gameClass = gameClass
        self.maxDepth = maxDepth
        self.transposition_table = TranspositionTable()

    def findBestMove(self, boardRepr, isMaximizingPlayer, dice=None):
        bestScore, bestMove = self.alphaBeta(boardRepr, self.maxDepth, float('-inf'), float('inf'), isMaximizingPlayer, dice=dice)
        return bestMove

    def alphaBeta(self, boardRepr, depth, alpha, beta, isMaximizingPlayer, dice=None):
        if self.gameClass.isGameOver(boardRepr):
            return self.heuristic(boardRepr), None
        if depth == 0:
            return self.heuristic(boardRepr), None

        transposition_value = self.transposition_table.lookup(boardRepr)
        if transposition_value:
            return transposition_value

        if isMaximizingPlayer:
            maxEval = float('-inf')
            bestMove = None
            if dice is not None:
                possibleMoves = self.gameClass.getPossibleMoves(boardRepr, dice=dice)
            else:
                possibleMoves = self.gameClass.getPossibleMoves(boardRepr)
            possibleMoves = sorted([ (self.heuristic(nextRepr), nextRepr, move) for nextRepr, move in possibleMoves ], reverse=True)
            if not possibleMoves:
                possibleMoves.append( (0, boardRepr, None) )
            for _, nextRepr, move in possibleMoves:
                if dice is not None:
                    eval = 0
                    for nextDice, prob in self.gameClass.diceStates():
                        eval += prob * self.alphaBeta(nextRepr, depth - 1, alpha, beta, False, dice=nextDice)[ 0 ]
                else:
                    eval, _ = self.alphaBeta(nextRepr, depth - 1, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table.store(boardRepr, (maxEval, bestMove))
            return maxEval, bestMove
        else:
            minEval = float('inf')
            bestMove = None
            if dice is not None:
                possibleMoves = self.gameClass.getPossibleMoves(boardRepr, dice=dice)
            else:
                possibleMoves = self.gameClass.getPossibleMoves(boardRepr)
            possibleMoves = sorted([ (self.heuristic(nextRepr), nextRepr, move) for nextRepr, move in possibleMoves ])
            if not possibleMoves:
                possibleMoves.append( (0, boardRepr, None) )
            for _, nextRepr, move in possibleMoves:
                if dice is not None:
                    eval = 0
                    for nextDice, prob in self.gameClass.diceStates():
                        eval += prob * self.alphaBeta(nextRepr, depth - 1, alpha, beta, True, dice=nextDice)[ 0 ]
                else:
                    eval, _ = self.alphaBeta(nextRepr, depth - 1, alpha, beta, True)
                if eval < minEval:
                    minEval = eval
                    bestMove = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table.store(boardRepr, (minEval, bestMove))
            return minEval, bestMove

    def heuristic(self, boardRepr):
        return self.gameClass.getScore(boardRepr)

class Human:
    def findBestMove(*args, **kwargs):
        return input()

if __name__ == '__main__':
    gameClass = Shatranj
    ai1 = AlphaBetaAI( gameClass, maxDepth=5 )
    ai2 = AlphaBetaAI( gameClass, maxDepth=5 )

    game = gameClass( 'Ali', 'Veli' )

    while True:
        print( game.board.boardToString() )
        if game.isGameOver(game.board.boardToFEN()):
            winner = game.winner(game.board.boardToFEN())
            if winner == 1:
                print( f'{game.board.players[0].name} wins' )
            if winner == -1:
                print( f'{game.board.players[1].name} wins' )
            if winner == 0:
                print( 'Draw' )
            break
        dice = None
        if gameClass.hasDice():
            dice = gameClass.rollDice()
            print( "Dice: ", dice )
        if game.board.currentTurn == game.board.players[0]:
            move = ai1.findBestMove( game.board.boardToFEN(), game.board.currentTurn == game.board.players[0], dice )
        else:
            move = ai2.findBestMove( game.board.boardToFEN(), game.board.currentTurn == game.board.players[0], dice )
        if dice is not None:
            game.play( move, dice )
        else:
            game.play( move )