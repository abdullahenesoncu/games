import shatranj.Heuristic
from shatranj.Board import Board

class AlphaBetaAI:
    def __init__( self, maxDepth=5 ):
        self.maxDepth = maxDepth
        self.cnt = 0
        self.dp = {}
        self.dp2 = {}

    def getHash( self, board ):
        return ' '.join( board.boardToFEN().split()[ :2 ] )

    def heuristic( self, board ):
        return board.getScore()

    def findBestMove( self, board ):
        currentColor = 'w' if board.currentTurn == board.players[ 0 ] else 'b'
        _, bestMove = self.abprune( board, 0, currentColor, float('-inf'), float('inf') )
        return bestMove

    def quiescence(self, board, color, alpha, beta):
        h = self.getHash(board)
        if h in self.dp2:
            return self.dp2[ h ]

        self.cnt += 1
        stand_pat = self.heuristic(board)
        if color == 'w':
            if stand_pat >= beta:
                self.dp2[ h ] = ( beta, None )
                return self.dp2[ h ]
            if alpha < stand_pat:
                alpha = stand_pat
        else:
            if stand_pat <= alpha:
                self.dp2[ h ] = ( alpha, None )
                return self.dp2[ h ]
            if beta > stand_pat:
                beta = stand_pat

        possibleMoves = [move for move in board.getPossibleMoves() if board.isCapture(move)]
        
        if color == 'w':
            maxScore = float( '-inf' )
            bestMove = None
            for move in possibleMoves:
                board.play( move )
                nextScore, _ = self.quiescence( board, 'b', alpha, beta )
                if bestMove == None or maxScore < nextScore:
                    maxScore = nextScore
                    bestMove = move
                board.undo()
                alpha = max( alpha, maxScore )
                if beta <= alpha:
                    break
            self.dp2[ h ] = ( maxScore, bestMove )
            return self.dp2[ h ]
        else:
            minScore = float( 'inf' )
            bestMove = None
            for move in possibleMoves:
                board.play( move )
                nextScore, _ = self.quiescence( board, 'w', alpha, beta )
                if bestMove == None or minScore > nextScore:
                    minScore = nextScore
                    bestMove = move
                board.undo()
                beta = min( beta, minScore )
                if beta <= alpha:
                    break
            self.dp2[ h ] = ( minScore, bestMove )
            return self.dp2[ h ]

    def abprune( self, board, depth, color, alpha, beta ):
        h = self.getHash( board ) + f" d: {depth}"
        if h in self.dp:
            return self.dp[ h ]

        self.cnt += 1
        if board.isGameOver():
            self.dp[ h ] = self.heuristic( board ), None
            return self.dp[ h ]
        if depth == self.maxDepth:
            self.dp[ h ] = self.quiescence(board, color, alpha, beta)
            return self.dp[ h ]

        bestMove = None
        possibleMoves = board.getPossibleMoves()
        possibleShahMoves = []
        possibleCaptureMoves = []
        possibleRegularMoves = []

        for move in possibleMoves:
            if board.isCapture( move ):
                possibleCaptureMoves.append( move )
            else:
                board.play( move )
                if board.isCheck():
                    possibleShahMoves.append( move )
                else:
                    possibleRegularMoves.append( ( self.heuristic( board ), move ) )
                board.undo()

        possibleRegularMoves.sort( reverse=(color == 'w') )
        possibleMoves = possibleShahMoves + possibleCaptureMoves + [ m[ 1 ] for m in possibleRegularMoves ]

        if color == 'w':
            maxScore = float( '-inf' )
            bestMove = None
            for move in possibleMoves:
                board.play( move )
                nextScore, _ = self.abprune( board, depth + 1, 'b', alpha, beta )
                if bestMove == None or maxScore < nextScore:
                    maxScore = nextScore
                    bestMove = move
                board.undo()
                alpha = max( alpha, maxScore )
                if beta <= alpha:
                    break
            self.dp[ h ] = ( maxScore, bestMove )
            return self.dp[ h ]
        else:
            minScore = float( 'inf' )
            bestMove = None
            for move in possibleMoves:
                board.play( move )
                nextScore, _ = self.abprune( board, depth + 1, 'w', alpha, beta )
                if bestMove == None or minScore > nextScore:
                    minScore = nextScore
                    bestMove = move
                board.undo()
                beta = min( beta, minScore )
                if beta <= alpha:
                    break
            self.dp[ h ] = ( minScore, bestMove )
            return self.dp[ h ]

if __name__ == '__main__':
    ai = AlphaBetaAI(maxDepth=5)
    
    board = Board.boardFromFEN( Board.getInitialRepr() )
    from datetime import datetime
    starttime = datetime.now()
    step = 0
    while True:
        print(board.boardToString())
        print(board.boardToFEN())
        if board.isGameOver():
            winner = board.winner()
            if winner is None:
                print('Draw')
            else:
                print(f'{winner.name} wins')
            print( step )
            break
        move = ai.findBestMove(board)
        board.play(move)
        step += 1
        print(ai.cnt)
        print(datetime.now() - starttime)
