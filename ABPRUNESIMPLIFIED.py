from shatranj.Game import Shatranj
from datetime import datetime
import random

class AlphaBetaAI:

    def __init__(self, gameClass, maxDepth=5):
        self.gameClass = gameClass
        self.maxDepth = maxDepth
        self.bestMove = None
        self.bestEval = None
    
    def getFenHash(self, fenRepr):
        return ' '.join(fenRepr.split()[:2])

    def findBestMove(self, boardRepr, isMaximizingPlayer, fens):
        self.bestMove = None
        self.bestEval = None
        alpha = float('-inf')
        beta = float('inf')
        self.find_move(boardRepr, self.maxDepth, alpha, beta, isMaximizingPlayer, fens)
        print(self.bestEval, self.bestMove)
        return self.bestMove
    
    def getBestMoves( self, moves ):
        arr = moves[ 3 : ]
        return moves[ : 3 ] + random.choices( arr, k = min( len( arr ), 3 ) )
    
    def find_move(self, boardRepr, depth, alpha, beta, isMaximizingPlayer, fens):
        if depth == 0:
            return self.heuristic(boardRepr)
            return self.captureSearch(boardRepr, alpha, beta, isMaximizingPlayer)

        if self.gameClass.isGameOver(boardRepr):
            return self.heuristic(boardRepr)

        possibleMoves = [pM for pM in self.gameClass.getPossibleMoves(boardRepr) if self.getFenHash(pM[0]) not in fens]
        orderedMoves = sorted([(self.heuristic(move[0], soft=True), move) for move in possibleMoves], reverse=isMaximizingPlayer)
        orderedMoves = self.getBestMoves( orderedMoves )
        
        for _, ( nextRepr, move ) in orderedMoves:
            score = -self.find_move(nextRepr, depth - 1, -beta, -alpha, not isMaximizingPlayer, fens)

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score
                if depth == self.maxDepth:
                    self.bestMove = move
                    self.bestEval = score

        return alpha
    
    def captureSearch(self, boardRepr, alpha, beta, isMaximizingPlayer):
        eval = self.heuristic(boardRepr)

        if eval >= beta:
            return beta

        if eval > alpha:
            alpha = eval

        possibleMoves = self.gameClass.getPossibleMoves(boardRepr)
        captureMoves = []

        for nextRepr, move in possibleMoves:
            if self.gameClass.isCapture( boardRepr, move ) or self.gameClass.isCheck( nextRepr ):
                captureMoves.append((self.heuristic(nextRepr, soft=True), (nextRepr, move)))

        captureMoves.sort(reverse=isMaximizingPlayer)

        for _, ( nextRepr, move ) in captureMoves:
            eval = -self.captureSearch(nextRepr, -beta, -alpha, not isMaximizingPlayer)

            if eval >= beta:
                return beta

            if eval > alpha:
                alpha = eval

        return alpha
    
    def heuristic(self, boardRepr, soft=False):
        return self.gameClass.getScore(boardRepr, soft=soft)

if __name__ == '__main__':
    gameClass = Shatranj
    ai = AlphaBetaAI(gameClass, maxDepth=5)

    game = gameClass('Ali', 'Veli')
    #from shatranj.Board import Board
    #game.board = Board.boardFromFEN('1v1s4/1S2v3/8/2v5/2v3v1/2v5/2v5/8 w 20 188')

    starttime = datetime.now()
    fens = []
    while True:
        print(game.board.boardToString())
        print(game.board.boardToFEN())
        fens.append(' '.join(game.board.boardToFEN().split()[:2]))
        if game.isGameOver(game.board.boardToFEN()):
            winner = game.winner(game.board.boardToFEN())
            if winner == 1:
                print(f'{game.board.players[0].name} wins')
            if winner == -1:
                print(f'{game.board.players[1].name} wins')
            if winner == 0:
                print('Draw')
            break
        move = ai.findBestMove(game.board.boardToFEN(), game.board.currentTurn == game.board.players[0], fens)
        game.play(move)
        print(ai.bestEval)
        print(datetime.now()-starttime)
