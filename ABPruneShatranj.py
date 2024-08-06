from shatranj.Game import Shatranj
from datetime import datetime
import random

class AlphaBetaAI:
    def __init__(self, gameClass, maxDepth=5):
        self.gameClass = gameClass
        self.maxDepth = maxDepth
        self.cnt = 0
        self.totalGetPosMoves = 0.0
    
    def getFenHash(self, fenRepr):
        return ' '.join(fenRepr.split()[:2])

    def findBestMove(self, boardRepr, isMaximizingPlayer, fens):
        bestScore, bestMove = self.negamax(boardRepr, self.maxDepth, float('-inf'), float('inf'), 1 if isMaximizingPlayer else -1, fens, firstMove=True)
        print(bestScore, bestMove)
        return bestMove
    
    def getSamplePossibleMoves(self, heuristicallySortedPossibleMoves):
        return heuristicallySortedPossibleMoves
        arr = heuristicallySortedPossibleMoves[3:]
        return heuristicallySortedPossibleMoves[:3] + random.sample(arr, min(len(arr), 3))
    
    def negamax(self, boardRepr, depth, alpha, beta, color, fens, firstMove=False):
        self.cnt += 1
        if self.gameClass.isGameOver(boardRepr):
            return self.heuristic(boardRepr), None
        if depth == 0:
            return self.heuristic( boardRepr, soft=False ), None
            return self.captureSearch(boardRepr, alpha, beta, color, fens)

        maxNext = float('-inf')
        bestMove = None
        possibleMoves = [pM for pM in self.gameClass.getPossibleMoves(boardRepr) if self.getFenHash(pM[0]) not in fens]
        possibleMovesOnlyCheck = [pM for pM in possibleMoves if self.gameClass.isCheck(pM[0])]
        if possibleMovesOnlyCheck and color==1:
            possibleMoves = possibleMovesOnlyCheck
        possibleMoves = sorted([(self.heuristic(nextRepr, soft=True), nextRepr, move) for nextRepr, move in possibleMoves], reverse=True)
        if not possibleMoves:
            possibleMoves.append((0, boardRepr, None))
        possibleMoves = self.getSamplePossibleMoves(possibleMoves)
        for _, nextRepr, move in possibleMoves:
            next, _ = self.negamax(nextRepr, depth - 1, -beta, -alpha, -color, fens)
            next = -next
            if next > maxNext:
                maxNext = next
                bestMove = move
            #alpha = max(alpha, next)
            #if beta <= alpha:
            #    break
        return maxNext, bestMove
    
    def captureSearch(self, boardRepr, alpha, beta, color, fens):
        self.cnt += 1

        maxEval = color * self.heuristic(boardRepr)
        bestMove = None
        possibleMoves = [pM for pM in self.gameClass.getPossibleMoves(boardRepr) if self.getFenHash(pM[0]) not in fens]
        possibleMoves = [pM for pM in possibleMoves if self.gameClass.isCapture(boardRepr, pM[1]) or self.gameClass.isCheck(pM[0])]
        possibleMoves = sorted([(color*-1*self.heuristic(nextRepr, soft=True), nextRepr, move) for nextRepr, move in possibleMoves])
        for score, nextRepr, move in possibleMoves:
            eval, _ = self.captureSearch(nextRepr, -beta, -alpha, -color, fens)
            eval = -eval
            if eval > maxEval:
                maxEval = eval
                bestMove = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, bestMove

    def heuristic(self, boardRepr, soft=False):
        color = 1 if 'w' in boardRepr else -1
        return color * self.gameClass.getScore(boardRepr, soft=soft)

if __name__ == '__main__':
    gameClass = Shatranj
    ai = AlphaBetaAI(gameClass, maxDepth=5)

    game = gameClass('Ali', 'Veli')
    from shatranj.Board import Board
    game.board = Board.boardFromFEN('1r1r4/8/1h6/2p5/2P5/1HS5/R3R3/1s6 b 0 1')
    game.board = Board.boardFromFEN('8/1p5s/3f4/8/2p5/p1P5/P1P2Pv1/5S2 w 2 89')
    #game.board = Board.boardFromFEN('1vr1sr2/5p2/2P1f1p1/pP4Fp/hp2H2R/h1pP2P1/P3VP2/SFv1HR2 w 0 1')
    game.board = Board.boardFromFEN('1vr2r2/5p2/2P1fHp1/pP1R2Fp/hp6/h1pP1HPs/P3VP2/SFv2R2 w 0 1') # 3. Mat sorusu son 3 hamle, 3 hamlede cozduk
    game.board = Board.boardFromFEN('1h1r4/6sP/1PpHf2f/2PvPFF1/3P2R1/1ph3R1/r5V1/2S5 w 0 1') # 4. Mat sorusu son 3 hamle, 9 hamlede cozduk
    game.board = Board.boardFromFEN('2r1hf2/8/fRp1pppp/s7/p1PSh1p1/P2FF1PP/1RHPH3/8 b 0 1') # 5. Mat sorusu son 3 hamle, 3 hamlede cozduk
    game.board = Board.boardFromFEN('1rf3V1/2Pp1H2/8/2Fp1V1R/1p1hPH2/p5s1/1rPpPp2/SFh3v1 w 0 1') # 6. Mat sorusu son 3 hamle, 3 hamlede cozduk
    game.board = Board.boardFromFEN('8/2p5/R1Vv4/pP3F1p/4pff1/FPP1s3/P3rrhR/1H1S4 w 0 1') # 7. Mat sorusu son 3 hamle, 3 hamlede cozduk
    game.board = Board.boardFromFEN('rff2vr1/hHHph3/1pp4p/5Pp1/4P3/sVPFF3/P2S4/R7 w 0 1') # 8. Mat sorusu son 3 hamle, 3 hamlede cozduk

    from datetime import datetime
    starttime = datetime.now()
    fens = []
    step = 0
    while True:
        print(game.board.boardToString())
        print(game.board.boardToFEN())
        # fens.append(' '.join(game.board.boardToFEN().split()[:2]))
        if game.isGameOver(game.board.boardToFEN()):
            winner = game.winner(game.board.boardToFEN())
            if winner == 1:
                print(f'{game.board.players[0].name} wins')
            if winner == -1:
                print(f'{game.board.players[1].name} wins')
            if winner == 0:
                print('Draw')
            print( step )
            break
        move = ai.findBestMove(game.board.boardToFEN(), game.board.currentTurn == game.board.players[0], fens)
        game.play(move)
        step += 1
        print(ai.cnt)
        print(game.ELLAPSED, game.CNT)
        print(datetime.now() - starttime)
