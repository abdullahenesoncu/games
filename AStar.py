from chess.Game import Chess, Board as ChessBoard
import heapq
import random

class ChessAStarAI:
    def __init__(self, gameClass, maxDepth=16):
        self.gameClass = gameClass
        self.maxDepth = maxDepth
        self.moveHistory = {}

    def findBestMove(self, boardRepr, isMaximizingPlayer):
        frontier = [(-self.heuristic(boardRepr, isMaximizingPlayer), 0, boardRepr, None)]
        cnt = 0
        bestMove = None
        bestScore = None
        while frontier:
            score, depth, repr, move = heapq.heappop(frontier)
            score = -score

            if (bestScore is None or score > bestScore) and move is not None:
                bestScore = score
                bestMove = move
            
            if score > 1e10:
                print(score)
                return move
            
            if score < -1e10:
                continue

            if cnt>=3000:
                return bestMove

            for nextRepr, m in self.gameClass.getPossibleMoves(repr):
                r = ' '.join( nextRepr.split()[:-2] )
                cnt += 1
                nextCost = self.heuristic(nextRepr, isMaximizingPlayer)
                if depth%2==0:
                    nextCost = max( nextCost, score )
                else:
                    nextCost = min( nextCost, score )
                heapq.heappush(frontier, (-nextCost, depth + 1, nextRepr, m if move is None else move))
        
        return bestMove
    
    def heuristic(self, boardRepr, isMaximizingPlayer):
        score = self.gameClass.getScore(boardRepr)
        return -score if isMaximizingPlayer else score

    def updateMoveHistory(self, boardRepr):
        r = ' '.join( boardRepr.split()[:-2] )
        self.moveHistory[r] = True

if __name__ == '__main__':
    random.seed(235212)
    gameClass = Chess
    ai1 = ChessAStarAI( gameClass )
    ai2 = ChessAStarAI( gameClass, maxDepth=3 )

    game = gameClass( 'White', 'Black' )

    while True:
        print( game.board.boardToString() )
        print( game.board.boardToFEN() )
        print( game.board.currentTurn.color )
        ai1.updateMoveHistory( game.board.boardToFEN() )
        ai2.updateMoveHistory( game.board.boardToFEN() )
        if game.board.isGameOver():
            print(game.board.isDraw())
            print('Checkmate:', game.board.isCheckmate( game.board.currentTurn ))
            break
        if game.board.currentTurn.color == 'white':
            move = ai1.findBestMove( game.board.boardToFEN(), game.board.currentTurn.color == 'white' )
        else:
            move = ai2.findBestMove( game.board.boardToFEN(), game.board.currentTurn.color == 'white' )
        game.play( move )