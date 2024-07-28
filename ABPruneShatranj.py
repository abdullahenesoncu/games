from shatranj.Game import Shatranj
from datetime import datetime
import random

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def lookup(self, key):
        return self.table.get(key)

    def store(self, key, value):
        self.table[key] = value

class AlphaBetaAI:
    def __init__(self, gameClass, maxDepth=5):
        self.gameClass = gameClass
        self.maxDepth = maxDepth
        self.transposition_table = TranspositionTable()
        self.cnt = 0
        self.totalGetPosMoves = 0.0
        self.path = []
    
    def getFenHash( self, fenRepr ):
        return ' '.join( fenRepr.split()[ : 2 ] )

    def findBestMove(self, boardRepr, isMaximizingPlayer):
        bestScore, bestMove = self.alphaBeta(boardRepr, self.maxDepth, float('-inf'), float('inf'), isMaximizingPlayer)
        return bestMove
    
    def getSamplePossibleMoves( self, heuristicallySortedPossibleMoves ):
        #return heuristicallySortedPossibleMoves
        arr = heuristicallySortedPossibleMoves[ 3 : ]
        return heuristicallySortedPossibleMoves[ : 3 ] + random.sample( arr, min( len( arr ) , 3 ) )
    
    def alphaBeta(self, boardRepr, depth, alpha, beta, isMaximizingPlayer):
        self.cnt += 1
        if self.gameClass.isGameOver(boardRepr):
            return self.heuristic(boardRepr), None
        if depth == 0:
            return self.heuristic(boardRepr), None

        transposition_value = self.transposition_table.lookup(boardRepr)
        if transposition_value:
            return transposition_value

        self.path.append( self.getFenHash( boardRepr ) )

        if isMaximizingPlayer:
            maxEval = float('-inf')
            bestMove = None
            possibleMoves = [ pM for pM in self.gameClass.getPossibleMoves(boardRepr) if self.getFenHash( pM[ 1 ] ) not in self.path ]
            possibleMoves = sorted([ (-self.heuristic(nextRepr), nextRepr, move) for nextRepr, move in possibleMoves ])
            if not possibleMoves:
                possibleMoves.append( (0, boardRepr, None) )
            possibleMoves = self.getSamplePossibleMoves( possibleMoves )
            for _, nextRepr, move in possibleMoves:
                eval, _ = self.alphaBeta( nextRepr, depth - 1, alpha, beta, False )
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table.store(boardRepr, (maxEval, bestMove))
            self.path.pop( len( self.path ) - 1 )
            return maxEval, bestMove
        else:
            minEval = float('inf')
            bestMove = None
            possibleMoves = [ pM for pM in self.gameClass.getPossibleMoves(boardRepr) if self.getFenHash( pM[ 1 ] ) not in self.path ]
            possibleMoves = sorted([ (self.heuristic(nextRepr), nextRepr, move) for nextRepr, move in possibleMoves ])
            if not possibleMoves:
                possibleMoves.append( (0, boardRepr, None) )
            possibleMoves = self.getSamplePossibleMoves( possibleMoves )
            for _, nextRepr, move in possibleMoves:
                eval, _ = self.alphaBeta( nextRepr, depth - 1, alpha, beta, True )
                if eval < minEval:
                    minEval = eval
                    bestMove = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table.store(boardRepr, (minEval, bestMove))
            self.path.pop( len( self.path ) - 1 )
            return minEval, bestMove

    def heuristic(self, boardRepr):
        return self.gameClass.getScore(boardRepr)

if __name__ == '__main__':
    gameClass = Shatranj
    ai = AlphaBetaAI( gameClass, maxDepth=7 )

    game = gameClass( 'Ali', 'Veli' )
    from shatranj.Board import Board
    # game.board = Board.boardFromFEN( '1r1r4/8/1h6/2p5/2P5/1HS5/R3R3/1s6 b 0 1' )
    # game.board = Board.boardFromFEN( '8/1p5s/3f4/8/2p5/p1P5/P1P2Pv1/5S2 w 2 89' )

    from datetime import datetime
    starttime = datetime.now()
    while True:
        print( game.board.boardToString() )
        print( game.board.boardToFEN() )
        if game.isGameOver(game.board.boardToFEN()):
            winner = game.winner(game.board.boardToFEN())
            if winner == 1:
                print( f'{game.board.players[0].name} wins' )
            if winner == -1:
                print( f'{game.board.players[1].name} wins' )
            if winner == 0:
                print( 'Draw' )
            break
        move = ai.findBestMove( game.board.boardToFEN(), game.board.currentTurn == game.board.players[0] )
        game.play( move )
        print( ai.cnt )
        print( game.ELLAPSED, game.CNT )
        print(datetime.now()-starttime)