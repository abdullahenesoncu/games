from chess.Game import Chess, Board as ChessBoard

class DfsAI:
    def __init__( self, gameClass ):
        self.gameClass = gameClass
        self.maxDepth = 2

    def findBestMove( self, boardRepr, depth, isMaximizingPlayer ):
        if depth == self.maxDepth:
            return self.gameClass.getScore( boardRepr ), None

        bestMove = None
        if isMaximizingPlayer:
            maxEval = float( '-inf' )
            for nextRepr, move in self.gameClass.getPossibleMoves( boardRepr ):
                evaluation = self.findBestMove( nextRepr, depth+1, False )[0]
                if evaluation > maxEval:
                    maxEval = evaluation
                    bestMove = move
            return maxEval, bestMove
        else:
            minEval = float( 'inf' )
            for nextRepr, move in self.gameClass.getPossibleMoves( boardRepr ):
                evaluation = self.findBestMove( nextRepr, depth+1, True )[0]
                if evaluation < minEval:
                    minEval = evaluation
                    bestMove = move
            return minEval, bestMove

gameClass = Chess
ai = DfsAI( gameClass )

game = gameClass( 'White', 'Black' )

while True:
    print( game.board.boardToString() )
    print( game.board.currentTurn.color )
    if game.board.isGameOver():
        print('Checkmate:', game.board.isCheckmate( game.board.currentTurn ))
        break
    _, move = ai.findBestMove( game.board.boardToFEN(), 0, game.board.currentTurn.color=='white' )
    print( game.board.boardToFEN(), move )
    game.play( move )