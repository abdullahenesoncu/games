from shatranj.Board import Board
from datetime import datetime

def getFenHash(fenRepr):
    return ' '.join(fenRepr.split()[:2])

class Node:
    def __init__( self, repr, score=None ):
        self.repr = repr
        self.score = score
        self.childs = []
    
    def addChild( self, node, move ):
        self.childs.append( ( node, move ) )

class DFSAI:
    def __init__(self, maxDepth=5):
        self.maxDepth = maxDepth
        self.cnt = 0

    def findBestMove(self, board, mateExpectedColor, states):
        currentColor = 'w' if board.currentTurn == board.players[ 0 ] else 'b'
        _, bestMove = self.dfs(board, 0, currentColor, mateExpectedColor, states)
        return bestMove

    def dfs(self, board, depth, color, mateExpectedColor, states):
        self.cnt += 1
        if board.isGameOver():
            if color != mateExpectedColor:
                return depth, None
            else:
                return float( 'inf' ), None
        if depth == self.maxDepth:
            return float( 'inf' ), None

        bestMove = None
        possibleMoves = board.getPossibleMoves()

        if color == mateExpectedColor:
            minMateDepth = float('inf')
            for move in possibleMoves:
                board.play( move )
                if not board.isCheck():
                    board.undo()
                    continue
                mateDepth, _ = self.dfs(board, depth + 1, 'b' if color == 'w' else 'w', mateExpectedColor, states)
                if bestMove is None or minMateDepth > mateDepth + 1:
                    minMateDepth = mateDepth + 1
                    bestMove = move
                board.undo()
            return minMateDepth, bestMove
        else:
            maxMateDepth = float('-inf')
            for move in possibleMoves:
                board.play( move )
                mateDepth, _ = self.dfs(board, depth + 1, 'b' if color == 'w' else 'w', mateExpectedColor, states)
                if bestMove is None or maxMateDepth < mateDepth + 1:
                    maxMateDepth = mateDepth + 1
                    bestMove = move
                board.undo()
            return maxMateDepth, bestMove

class Mate:
    def __init__( self, initialFen, mateExpectedColor, expectedMoveNumber ):
        self.initialFen = initialFen
        self.mateExpectedColor = mateExpectedColor
        self.expectedMoveNumber = expectedMoveNumber

    def run( self, verbose=False ):
        starttime = datetime.now()
        ai = DFSAI( maxDepth=self.expectedMoveNumber )

        board = Board.boardFromFEN( self.initialFen )

        if verbose:
            print( '#' * 120 )

        step = 0
        states = []
        while True:
            if verbose:
                print(board.boardToString())
                print(board.boardToFEN())

            if board.isGameOver():
                winner = board.winner()
                print()
                assert( ( 'w' if winner == board.players[ 0 ]  else 'b' ) == self.mateExpectedColor )
                assert( step <= self.expectedMoveNumber )
                if verbose:
                    if winner == 1:
                        print(f'{board.players[0].name} wins')
                    if winner == -1:
                        print(f'{board.players[1].name} wins')
                    if winner == 0:
                        print('Draw')
                    print( f'mate found in {step}' )
                break

            move = ai.findBestMove(board, self.mateExpectedColor, states)
            if verbose:
                print( move )
            board.play( move )
            step += 1
            print(ai.cnt)
        print(datetime.now()-starttime)


if __name__ == '__main__':

    mate = Mate( '1vr2r2/5p2/2P1fHp1/pP1R2Fp/hp6/h1pP1HPs/P3VP2/SFv2R2 w 0 1', 'w', 3 ) # 3. Mat sorusu
    mate.run( verbose=True )

    mate = Mate( '1h1r4/6sP/1PpHf2f/2PvPFF1/3P2R1/1ph3R1/r5V1/2S5 w 0 1', 'w', 9 ) # 4. Mat sorusu
    mate.run( verbose=True )

    mate = Mate( '2r1hf2/8/fRp1pppp/s7/p1PSh1p1/P2FF1PP/1RHPH3/8 b 0 1', 'b', 3 ) # 5. Mat sorusu
    mate.run( verbose=True )

    mate = Mate( '1rf3V1/2Pp1H2/8/2Fp1V1R/1p1hPH2/p5s1/1rPpPp2/SFh3v1 w 0 1', 'w', 3 ) # 6. Mat sorusu
    mate.run( verbose=True )

    mate = Mate( '8/2p5/R1Vv4/pP3F1p/4pff1/FPP1s3/P3rrhR/1H1S4 w 0 1', 'w', 3 ) # 7. Mat sorusu
    mate.run( verbose=True )

    mate = Mate( 'rff2vr1/hHHph3/1pp4p/5Pp1/4P3/sVPFF3/P2S4/R7 w 0 1', 'w', 3 ) # 8. Mat sorusu
    mate.run( verbose=True )

    mate = Mate( '2f1V2V/FpvRPSRV/2hf1H1s/1r4p1/4P1P1/p2P4/8/rv6 b 0 1', 'b', 3 ) # 9. Mat sorusu
    mate.run( verbose=True )

    mate = Mate( '2f5/vs6/4p1V1/pF4pP/PfSpP1P1/1P6/2R1H1R1/2Fr2H1 b 0 1', 'b', 3 ) # 10. Mat sorusu
    mate.run( verbose=True )

    mate = Mate( '7R/5H2/4VP2/5F2/3phs1p/Fpp2V2/r3rp1P/3S2H1 w 0 1', 'w', 3 ) # 11. Mat sorusu
    mate.run( verbose=True )

    mate = Mate( '4s1f1/R3HHp1/1p3h1f/6Fh/1P2P3/1p1F1Pv1/1P3rPr/3S4 w 0 1', 'w', 3 ) # 12. Mat sorusu
    mate.run( verbose=True )

