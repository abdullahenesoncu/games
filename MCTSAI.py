import random
import math
from checker.Game import Checker
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Pipe, cpu_count
from threading import Lock
from tictactoe.Game import TicTacToe
from qirkat.Game import Qirkat

class Node:
    def __init__(self, board_state, gameClass, parent=None, move=None):
        self.board_state = board_state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.gameClass = gameClass
        self.untried_moves = gameClass.getPossibleMoves(board_state)

    def is_leaf(self):
        return len(self.children) == 0

    def add_child(self, move, board_state):
        child_node = [ c for c in self.children if c.move==move ]
        if child_node: return child_node[0]
        child_node = Node(board_state, self.gameClass, self, move)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        self.visits += 1
        self.wins += 1 if result > 0 else (0 if result == 0 else -1)


class MCTSAI:
    def __init__(self, gameClass, iterations=100):
        self.gameClass = gameClass
        self.iterations = iterations

    def mcts_iteration(self, node, simulate_pool, mutex, isMaximizingPlayer):
        mutex.acquire()
        while not node.is_leaf():
            node = self.select_child(node)

        nextRepr = node.board_state
        move = node.move
        if not self.gameClass.isGameOver(node.board_state):
            nextRepr, move = random.choice(node.untried_moves)
        mutex.release()
        
        future = simulate_pool.submit(self.simulate_random_gameplay, nextRepr, isMaximizingPlayer)
        score = future.result()

        mutex.acquire()
        try:
            node = node.add_child(move, nextRepr)
            while node is not None:
                node.update(score)
                node = node.parent
        finally:
            mutex.release()

    def findBestMove(self, boardRepr, isMaximizingPlayer):
        root = Node(boardRepr, self.gameClass)        
        mutex = Lock()

        # Create a process pool for simulations
        with ProcessPoolExecutor(max_workers=cpu_count()) as simulate_pool:
            # Distribute the iterations across multiple threads
            with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
                futures = [executor.submit(self.mcts_iteration, root, simulate_pool, mutex, isMaximizingPlayer) for _ in range(self.iterations)]
                for future in futures:
                    future.result()

        return max(root.children, key=lambda c: c.visits).move

    def select_child(self, node):
        best_value = float('-inf')
        best_nodes = []
        for child in node.children:
            uct_value = (child.wins / child.visits) + math.sqrt(2) * math.sqrt(math.log(node.visits) / child.visits)
            if uct_value > best_value:
                best_value = uct_value
                best_nodes = [child]
            elif uct_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes)

    def simulate_random_gameplay(self, repr, isMaximizingPlayer, maxDepth=10):
        depth = 0
        while not self.gameClass.isGameOver(repr) and depth < maxDepth:
            possible_moves = self.gameClass.getPossibleMoves(repr)
            if not possible_moves:
                break
            
            # Calculate scores for each possible move
            move_scores = [(move, self.gameClass.getScore(nextRepr)) for nextRepr, move in possible_moves]

            # Normalize scores to get probabilities
            total_score = sum(score for _, score in move_scores)
            if total_score > 0:
                probabilities = [score / total_score for _, score in move_scores]
            else:
                probabilities = [1 / len(move_scores) for _ in move_scores]  # Equal probability if all scores are non-positive

            # Choose a move based on the calculated probabilities
            nextRepr, chosen_move = random.choices(possible_moves, weights=probabilities, k=1)[0]
            repr = nextRepr
            depth += 1
        if isMaximizingPlayer:
            return self.gameClass.getScore(repr)
        else:
            return -self.gameClass.getScore(repr)

if __name__ == '__main__':
    gameClass = Qirkat
    ai1 = MCTSAI(gameClass)
    ai2 = MCTSAI(gameClass)

    game = gameClass( 'White', 'Black' )

    while True:
        print( game.board.dump() )
        if game.isGameOver(game.board.dumpFEN()):
            winner = game.winner(game.board.dumpFEN())
            if winner == 1:
                print( 'White wins' )
            if winner == -1:
                print( 'Black wins' )
            if winner == 0:
                print( 'Draw' )
            break
        if game.board.currentTurn == game.board.players[0]:
            move = ai1.findBestMove( game.board.dumpFEN(), game.board.currentTurn == game.board.players[0] )
        else:
            move = ai2.findBestMove( game.board.dumpFEN(), game.board.currentTurn == game.board.players[0] )
        game.play( move )
