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

dp = {}
dirs = [(1,2), (2,1), (-1,2), (-2,1), (1,-2), (2,-1), (-1,-2), (-2,-1)]
def f( m, n, x, y ):
   if ( m, n, x, y ) in dp: return dp[ ( m, n, x, y ) ]
   if m * n < 20 * 20:
      return dfs_knights_tour( y*n+x, [ y * n + x ], ( 1 << (y*x+x) ), m, n )
   if m >= n:
      m1 = m // 2
      m2 = m - m1
      for Y in reversed(list(range( m1 ))):
         for X in reversed(list(range( n ))):
            for dirX, dirY in dirs:
               if 0 <= X+dirX < n and m1 <= Y+dirY < m:
                  path1 = f( m1, n, X, Y )
                  if not path1: continue
                  path1 = list( reversed( path1 ) )
                  path2 = f( m2, n, X+dirX, Y+dirY-m1 )
                  if not path2: continue
                  res = [*path1]
                  print(res[-1]%n, res[-1]//n)
                  print("AAAAAA")
                  print(X,Y,dirX,dirY)
                  for p in path2:
                     x = p % n
                     y = p // n + m1
                     print(x,y)
                     res.append( y * n + x )
                  dp[ ( m, n, x, y ) ] = res
                  return res

   n1 = n // 2
   n2 = n - n1
   for y in reversed(list(range( m ))):
      for x in reversed(list(range( n1 ))):
         for dirX, dirY in dirs:
            if n1 <= x+dirX < n and 0 <= y+dirY < m:
               path1 = f( m, n1, x, y )
               if not path1: continue
               path1 = list( reversed( path1 ) )
               path2 = f( m, n2, x+dirX-n1, y+dirY )
               if not path2: continue
               res = []
               for p in path1:
                  x = p % n1
                  y = p // n1
                  res.append( y * n + x )
               for p in path2:
                  x = p % n2 + n1
                  y = p // n2
                  res.append( y * n + x )
               dp[ ( m, n, x, y ) ] = res
               return res
   
   return None

m, n = 30, 30
import sys
sys.setrecursionlimit(m*n*2)
start_position = 0
vis = (1 << start_position)
path = [start_position]
tour_path = f(m, n, 0, 0)

lastx, lasty = None, None
import math

if tour_path:
    route = [(p % n, p // n) for p in tour_path]
    for i in range( len(route)-1 ):
        if abs(route[i][0]-route[i+1][0]) + abs(route[i][1]-route[i+1][1]) == 3 and abs(abs(route[i][0]-route[i+1][0]) - abs(route[i][1]-route[i+1][1]))==1:
           pass
        else:
           print(route[i], route[i+1])
           assert(False)
    print(route)
else:
    print(None)