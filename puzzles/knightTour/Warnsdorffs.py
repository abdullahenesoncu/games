def knight_moves(position, m, n):
    """ Returns possible moves for a knight from a given position on an m x n chessboard. """
    x, y = position % n, position // n
    potential_moves = [
        (x + 2, y + 1), (x + 2, y - 1),
        (x - 2, y + 1), (x - 2, y - 1),
        (x + 1, y + 2), (x + 1, y - 2),
        (x - 1, y + 2), (x - 1, y - 2)
    ]
    return [ny * n + nx for nx, ny in potential_moves if 0 <= nx < n and 0 <= ny < m]

def count_onward_moves(position, vis, m, n):
    """ Counts the number of unvisited onward moves from a given position. """
    return sum(not (vis & (1 << move)) for move in knight_moves(position, m, n))

def dfs_knights_tour(position, path, vis, m, n):
    """ Implements DFS with Warnsdorff's heuristic to find the Knight's Tour. """
    if len(path) == m * n:
        return path

    next_moves = knight_moves(position, m, n)
    # Sort moves based on Warnsdorff's heuristic (fewest onward moves first)
    next_moves.sort(key=lambda move: count_onward_moves(move, vis, m, n))

    for move in next_moves:
        if not (vis & (1 << move)):
            new_vis = vis | (1 << move)
            path.append(move)
            result = dfs_knights_tour(move, path, new_vis, m, n)
            if result:
                return result
            path.pop()

    return None

m, n = 10, 10
import sys
sys.setrecursionlimit(m*n*2)
start_position = 0
vis = (1 << start_position)
path = [start_position]
tour_path = dfs_knights_tour(start_position, path, vis, m, n)

d = {}
i = 0
if tour_path:
    d = {(p%n, p//n): i for i, p in enumerate(tour_path) }
    print(d)
    #print([(p % n, p // n) for p in tour_path])
    for i in range(m):
        for j in range(n):
            print( f'{d[(i,j)]:3}', end=' ' )
        print()
else:
    print(None)
