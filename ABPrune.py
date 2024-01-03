from tictactoe.Game import TicTacToe
from qirkat.Game import Qirkat
from checker.Game import Checker
from nineMenMorris.Game import NineMenMorris
import random

class AlphaBetaAI:
    def __init__(self, gameClass, maxDepth=10):
        self.gameClass = gameClass
        self.maxDepth = maxDepth

    def findBestMove(self, boardRepr, isMaximizingPlayer):
        bestScore, bestMove = self.alphaBeta(boardRepr, self.maxDepth, float('-inf'), float('inf'), isMaximizingPlayer)
        return bestMove

    def alphaBeta(self, boardRepr, depth, alpha, beta, isMaximizingPlayer):
        if self.gameClass.isGameOver(boardRepr):
            return self.heuristic(boardRepr), None
        if depth == 0:
            return self.heuristic(boardRepr), None

        if isMaximizingPlayer:
            maxEval = float('-inf')
            bestMove = None
            possibleMoves = sorted([ (self.heuristic(nextRepr), nextRepr, move) for nextRepr, move in self.gameClass.getPossibleMoves(boardRepr) ], reverse=True)
            for _, nextRepr, move in possibleMoves:
                eval, _ = self.alphaBeta(nextRepr, depth - 1, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, bestMove
        else:
            minEval = float('inf')
            bestMove = None
            possibleMoves = [ (self.heuristic(nextRepr), nextRepr, move) for nextRepr, move in self.gameClass.getPossibleMoves(boardRepr) ]
            for _, nextRepr, move in possibleMoves:
                eval, _ = self.alphaBeta(nextRepr, depth - 1, alpha, beta, True)
                if eval < minEval:
                    minEval = eval
                    bestMove = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, bestMove

    def heuristic(self, boardRepr):
        return self.gameClass.getScore(boardRepr)

if __name__ == '__main__':
    gameClass = TicTacToe
    ai1 = AlphaBetaAI( gameClass, maxDepth=10 )
    ai2 = AlphaBetaAI( gameClass, maxDepth=10 )

    game = gameClass( 3, 'White', 'Black' )

    while True:
        print( game.board.boardToString() )
        if game.isGameOver(game.board.boardToFEN()):
            winner = game.winner(game.board.boardToFEN())
            if winner == 1:
                print( 'White wins' )
            if winner == -1:
                print( 'Black wins' )
            if winner == 0:
                print( 'Draw' )
            break
        if game.board.currentTurn == game.board.players[0]:
            move = ai1.findBestMove( game.board.boardToFEN(), game.board.currentTurn == game.board.players[0] )
        else:
            move = ai2.findBestMove( game.board.boardToFEN(), game.board.currentTurn == game.board.players[0] )
        game.play( move )