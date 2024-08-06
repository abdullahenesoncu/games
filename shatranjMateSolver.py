from shatranj.Game import Shatranj
from shatranj.Board import Board

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

    def findBestMove(self, boardRepr, mateExpectedColor, states):
        _, bestMove = self.dfs(boardRepr, 0, boardRepr.split()[ 1 ], mateExpectedColor, states)
        return bestMove
    
    def dfs(self, boardRepr, depth, color, mateExpectedColor, states):
        self.cnt += 1
        if Shatranj.isGameOver(boardRepr):
            if color != mateExpectedColor:
                return depth, None
            else:
                return float( 'inf' ), None
        if depth == self.maxDepth:
            return float( 'inf' ), None

        bestMove = None
        possibleMoves = [ pM for pM in Shatranj.getPossibleMoves( boardRepr ) if getFenHash( pM[ 0 ] ) not in states or True ]
        if color==mateExpectedColor:
            possibleMoves = [ pM for pM in possibleMoves if Shatranj.isCheck( pM[0] ) ]
        
        if color == mateExpectedColor:
            minMateDepth = float('inf')
            for nextRepr, move in possibleMoves:
                states.append( nextRepr )
                mateDepth, _ = self.dfs(nextRepr, depth + 1, 'b', mateExpectedColor, states)
                states.pop()
                if minMateDepth >= mateDepth + 1:
                    minMateDepth = mateDepth + 1
                    bestMove = move
            return minMateDepth, bestMove
        else:
            maxMateDepth = float('-inf')
            for nextRepr, move in possibleMoves:
                states.append( nextRepr )
                mateDepth, _ = self.dfs(nextRepr, depth + 1, 'w', mateExpectedColor, states)
                states.pop()
                if maxMateDepth <= mateDepth + 1:
                    maxMateDepth = mateDepth + 1
                    bestMove = move
            return maxMateDepth, bestMove

class Mate:
    def __init__( self, initialFen, mateExpectedColor, expectedMoveNumber ):
        self.initialFen = initialFen
        self.mateExpectedColor = mateExpectedColor
        self.expectedMoveNumber = expectedMoveNumber
    
    def run( self, verbose=False ):
        ai = DFSAI( maxDepth=self.expectedMoveNumber )

        game = Shatranj('Ali', 'Veli')
        game.board = Board.boardFromFEN( self.initialFen )

        if verbose:
            print( '#' * 120 )

        step = 0
        states = []
        while True:
            if verbose:
                print(game.board.boardToString())
                print(game.board.boardToFEN())
            
            if game.isGameOver(game.board.boardToFEN()):
                winner = game.winner(game.board.boardToFEN())
                assert( ( 'w' if winner == 1 else 'b' ) == self.mateExpectedColor )
                assert( step <= self.expectedMoveNumber )
                if verbose:
                    if winner == 1:
                        print(f'{game.board.players[0].name} wins')
                    if winner == -1:
                        print(f'{game.board.players[1].name} wins')
                    if winner == 0:
                        print('Draw')
                    print( f'mate found in {step}' )
                break
            
            states.append( getFenHash( game.board.boardToFEN() ) )
            move = ai.findBestMove(game.board.boardToFEN(), self.mateExpectedColor, states)
            game.play(move)
            step += 1
            print(ai.cnt)


if __name__ == '__main__':

    mate = Mate( '1r4s1/8/5PP1/S1h5/6HR/7F/1r2p3/7R w 0 1', 'w', 9 )
    mate.run( verbose=True )

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

