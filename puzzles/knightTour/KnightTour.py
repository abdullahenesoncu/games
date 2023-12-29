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

def dfs_knights_tour(position, path, vis, m, n):
    """ Implements DFS to find the Knight's Tour on a chessboard of given size using bit operations. """
    if len(path) == m * n:
        return path

    for move in knight_moves(position, m, n):
        if not (vis & (1 << move)):
            new_vis = vis | (1 << move)
            path.append(move)
            result = dfs_knights_tour(move, path, new_vis, m, n)
            if result:
                return result
            path.pop()

    return None

m, n = 7, 7
start_position = 0
vis = (1 << start_position)
path = [start_position]
tour_path = dfs_knights_tour(start_position, path, vis, m, n)

if tour_path:
    print([(p % n, p // n) for p in tour_path])
else:
    print(None)
