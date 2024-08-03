from shatranj.Game import Shatranj
from datetime import datetime
import random

class AlphaBetaAI:
    def __init__(self, gameClass, maxDepth=5):
        self.gameClass = gameClass
        self.maxDepth = maxDepth
        self.cnt = 0
        self.totalGetPosMoves = 0.0
    
    def getFenHash( self, fenRepr ):
        return ' '.join( fenRepr.split()[ : 2 ] )

    def findBestMove(self, boardRepr, isMaximizingPlayer, fens):
        bestScore, bestMove = self.alphaBeta(boardRepr, self.maxDepth, float('-inf'), float('inf'), isMaximizingPlayer, fens, firstMove=True)
        print( bestScore, bestMove )
        return bestMove
    
    def getSamplePossibleMoves( self, heuristicallySortedPossibleMoves ):
        #return heuristicallySortedPossibleMoves
        arr = heuristicallySortedPossibleMoves[ 3 : ]
        return heuristicallySortedPossibleMoves[ : 3 ] + random.sample( arr, min( len( arr ) , 3 ) )
    
    def alphaBeta(self, boardRepr, depth, alpha, beta, isMaximizingPlayer, fens, firstMove=False):
        self.cnt += 1
        if not firstMove and abs( self.heuristic(boardRepr) ) > 100:
            return self.heuristic(boardRepr), None
        if self.gameClass.isGameOver(boardRepr):
            return self.heuristic(boardRepr), None
        if depth == 0:
            return self.heuristic(boardRepr), None

        if isMaximizingPlayer:
            maxEval = float('-inf')
            bestMove = None
            possibleMoves = [ pM for pM in self.gameClass.getPossibleMoves(boardRepr) if self.getFenHash( pM[ 1 ] ) not in fens ]
            possibleMoves = sorted([ (-self.heuristic(nextRepr, soft=True), nextRepr, move) for nextRepr, move in possibleMoves ])
            if not possibleMoves:
                possibleMoves.append( (0, boardRepr, None) )
            possibleMoves = self.getSamplePossibleMoves( possibleMoves )
            for score, nextRepr, move in possibleMoves:
                eval, _ = self.alphaBeta( nextRepr, depth - 1, alpha, beta, False, fens )
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
            possibleMoves = [ pM for pM in self.gameClass.getPossibleMoves(boardRepr) if self.getFenHash( pM[ 1 ] ) not in fens ]
            possibleMoves = sorted([ (self.heuristic(nextRepr, soft=True), nextRepr, move) for nextRepr, move in possibleMoves ])
            if not possibleMoves:
                possibleMoves.append( (0, boardRepr, None) )
            possibleMoves = self.getSamplePossibleMoves( possibleMoves )
            for score, nextRepr, move in possibleMoves:
                eval, _ = self.alphaBeta( nextRepr, depth - 1, alpha, beta, True, fens )
                if eval < minEval:
                    minEval = eval
                    bestMove = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, bestMove

    def heuristic(self, boardRepr, soft=False):
        return self.gameClass.getScore(boardRepr, soft=soft)

if __name__ == '__main__':
    gameClass = Shatranj
    ai = AlphaBetaAI( gameClass, maxDepth=11 )

    game = gameClass( 'Ali', 'Veli' )
    from shatranj.Board import Board
    # game.board = Board.boardFromFEN( '1r1r4/8/1h6/2p5/2P5/1HS5/R3R3/1s6 b 0 1' )
    # game.board = Board.boardFromFEN( '8/1p5s/3f4/8/2p5/p1P5/P1P2Pv1/5S2 w 2 89' )
    game.board = Board.boardFromFEN( '1v1s4/1S2v3/8/2v5/2v3v1/2v5/2v5/8 w 20 188' )

    from datetime import datetime
    starttime = datetime.now()
    fens = []
    while True:
        print( game.board.boardToString() )
        print( game.board.boardToFEN() )
        fens.append( ' '.join( game.board.boardToFEN().split()[ : 2 ] ) )
        if game.isGameOver(game.board.boardToFEN()):
            winner = game.winner(game.board.boardToFEN())
            if winner == 1:
                print( f'{game.board.players[0].name} wins' )
            if winner == -1:
                print( f'{game.board.players[1].name} wins' )
            if winner == 0:
                print( 'Draw' )
            break
        move = ai.findBestMove( game.board.boardToFEN(), game.board.currentTurn == game.board.players[0], fens )
        game.play( move )
        print( ai.cnt )
        print( game.ELLAPSED, game.CNT )
        print(datetime.now()-starttime)