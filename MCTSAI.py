import random
import math
from checker.Game import Checker
from tictactoe.Game import TicTacToe
from qirkat.Game import Qirkat
from nineMenMorris.Game import NineMenMorris
from shatranj.Game import Shatranj

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
        child_node = [c for c in self.children if c.move == move]
        if child_node:
            return child_node[0]
        child_node = Node(board_state, self.gameClass, self, move)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        self.visits += 1
        self.wins += result

class MCTSAI:
    def __init__(self, gameClass, iterations=1000):  # Increased iterations
        self.gameClass = gameClass
        self.iterations = iterations

    def mcts_iteration(self, node, isMaximizingPlayer):
        while not node.is_leaf():
            node = self.select_child(node)

        next_board_state = node.board_state
        move = node.move
        if not self.gameClass.isGameOver(node.board_state):
            next_board_state, move = random.choice(node.untried_moves)

        score = self.simulate_random_gameplay(next_board_state, isMaximizingPlayer)

        node = node.add_child(move, next_board_state)
        while node is not None:
            node.update(score)
            node = node.parent

    def findBestMove(self, board_state, isMaximizingPlayer):
        root = Node(board_state, self.gameClass)
        for _ in range(self.iterations):
            self.mcts_iteration(root, isMaximizingPlayer)

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

    def simulate_random_gameplay(self, board_state, isMaximizingPlayer, maxDepth=20):
        depth = 0
        while not self.gameClass.isGameOver(board_state) and depth < maxDepth:
            possible_moves = self.gameClass.getPossibleMoves(board_state)
            if not possible_moves:
                break
            # Favor moves that could lead to a win in the simulation
            win_move = next((move for move in possible_moves), None)
            if win_move:
                board_state, _ = win_move
            else:
                board_state, _ = random.choice(possible_moves)
            depth += 1
        if not self.gameClass.isGameOver(board_state):
            return 0.5
        winner = self.gameClass.winner(board_state)
        return winner if isMaximizingPlayer else -winner

if __name__ == '__main__':
    gameClass = Shatranj
    ai1 = MCTSAI(gameClass)
    ai2 = MCTSAI(gameClass)

    game = gameClass('White', 'Black')

    from shatranj.Board import Board
    game.board = Board.boardFromFEN('1r1r4/8/1h6/2p5/2P5/1HS5/R3R3/1s6 b 0 1')

    while True:
        print(game.board.boardToString())
        print(game.board.boardToFEN())
        if game.isGameOver(game.board.boardToFEN()):
            winner = game.winner(game.board.boardToFEN())
            if winner == 1:
                print('White wins')
            elif winner == -1:
                print('Black wins')
            else:
                print('Draw')
            break
        if game.board.currentTurn == game.board.players[0]:
            move = ai1.findBestMove(game.board.boardToFEN(), game.board.currentTurn == game.board.players[0])
        else:
            move = ai2.findBestMove(game.board.boardToFEN(), game.board.currentTurn == game.board.players[0])
        game.play(move)
