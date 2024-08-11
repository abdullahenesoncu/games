import shatranj.Heuristic
from shatranj.Board import Board
import random

class AlphaBetaAI:
    def __init__( self, maxDepth=5 ):
        self.maxDepth = maxDepth
        self.cnt = 0

    def heuristic( self, board ):
        return board.getScore()

    def findBestMove( self, board ):
        currentColor = 'w' if board.currentTurn == board.players[ 0 ] else 'b'
        _, bestMove = self.abprune( board, 0, currentColor, float('-inf'), float('inf') )
        return bestMove

    def abprune( self, board, depth, color, alpha, beta ):
        self.cnt += 1
        if board.isGameOver():
            return self.heuristic( board ), None
        if depth == self.maxDepth:
            return self.heuristic( board ), None

        bestMove = None
        possibleMoves = board.getPossibleMoves()
        possibleShahMoves = []
        possibleCaptureMoves = []
        possibleRegularMoves = []

        for move in possibleMoves:
            if False and board.isCapture( move ):
                possibleCaptureMoves.append( move )
            else:
                board.play( move )
                if board.isCheck():
                    possibleShahMoves.append( move )
                else:
                    possibleRegularMoves.append( ( self.heuristic( board ), move ) )
                board.undo()

        possibleMoves = possibleShahMoves + possibleCaptureMoves
        if len( possibleMoves ) < 10:
            possibleRegularMoves.sort( reverse=( color == 'w' ) )
            possibleMoves += [ m[ 1 ] for m in possibleRegularMoves[ : 10 - len( possibleMoves ) ] ]

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
                    break  # Beta cut-off
            return maxScore, bestMove
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
                    break  # Alpha cut-off
            return minScore, bestMove

if __name__ == '__main__':
    ai = AlphaBetaAI(maxDepth=5)
    
    '''
    game.board = Board.boardFromFEN('1r1r4/8/1h6/2p5/2P5/1HS5/R3R3/1s6 b 0 1')
    game.board = Board.boardFromFEN('8/1p5s/3f4/8/2p5/p1P5/P1P2Pv1/5S2 w 2 89')
    #game.board = Board.boardFromFEN('1vr1sr2/5p2/2P1f1p1/pP4Fp/hp2H2R/h1pP2P1/P3VP2/SFv1HR2 w 0 1')
    game.board = Board.boardFromFEN('1vr2r2/5p2/2P1fHp1/pP1R2Fp/hp6/h1pP1HPs/P3VP2/SFv2R2 w 0 1') # 3. Mat sorusu son 3 hamle, 3 hamlede cozduk
    game.board = Board.boardFromFEN('1h1r4/6sP/1PpHf2f/2PvPFF1/3P2R1/1ph3R1/r5V1/2S5 w 0 1') # 4. Mat sorusu son 3 hamle, 9 hamlede cozduk
    game.board = Board.boardFromFEN('2r1hf2/8/fRp1pppp/s7/p1PSh1p1/P2FF1PP/1RHPH3/8 b 0 1') # 5. Mat sorusu son 3 hamle, 3 hamlede cozduk
    game.board = Board.boardFromFEN('1rf3V1/2Pp1H2/8/2Fp1V1R/1p1hPH2/p5s1/1rPpPp2/SFh3v1 w 0 1') # 6. Mat sorusu son 3 hamle, 3 hamlede cozduk
    game.board = Board.boardFromFEN('8/2p5/R1Vv4/pP3F1p/4pff1/FPP1s3/P3rrhR/1H1S4 w 0 1') # 7. Mat sorusu son 3 hamle, 3 hamlede cozduk
    game.board = Board.boardFromFEN('rff2vr1/hHHph3/1pp4p/5Pp1/4P3/sVPFF3/P2S4/R7 w 0 1') # 8. Mat sorusu son 3 hamle, 3 hamlede cozduk
    '''
    board = Board.boardFromFEN( Board.getInitialRepr() )
    from datetime import datetime
    starttime = datetime.now()
    fens = []
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
