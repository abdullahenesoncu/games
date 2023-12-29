import heapq

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

def heuristic(path, vis, m, n):
    # Heuristic based on Warnsdorff's rule - prioritize the move with fewer onward moves
    if len(path) < m * n:
        last_move = path[-1]
        return count_onward_moves(last_move, vis, m, n)
    return 0  # if path is complete, return 0

def a_star_knights_tour(x, y, m, n):
    pq = []  # Priority queue

    start = y * n + x
    vis = (1 << start)
    heapq.heappush(pq, (0, [start], vis))

    while pq:
        cost, path, vis = heapq.heappop(pq)

        if len(path) == m * n:
            return path

        for move in knight_moves(path[-1], m, n):
            if not (vis & (1 << move)):
                new_vis = vis | (1 << move)
                new_path = path + [move]
                new_cost = len(new_path) + heuristic(new_path, new_vis, m, n)
                heapq.heappush(pq, (new_cost, new_path, new_vis))

    return None

# Example usage:
m, n = 5, 5  # Smaller board for demonstration; large boards are computationally intensive
start_x, start_y = 0, 0
tour_path = a_star_knights_tour(start_x, start_y, m, n)

if tour_path:
    print([(p % n, p // n) for p in tour_path])
else:
    print(None)
