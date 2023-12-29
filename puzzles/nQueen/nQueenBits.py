def solve_n_queens_bitwise(n):
   def solve(row, columns, left_diagonals, right_diagonals):
      if row == n:
         # All queens are placed successfully
         solution = [0] * n
         for r in range(n):
               solution[r] = board[r]
         return solution

      # Available positions (0s) in the current row
      available_positions = ((1 << n) - 1) & ~(columns | left_diagonals | right_diagonals)

      while available_positions:
         # Position the next queen in the rightmost available spot
         position = available_positions & -available_positions
         available_positions -= position
         board[row] = position
         solution = solve(row + 1, 
                     columns | position, 
                     (left_diagonals | position) << 1, 
                     (right_diagonals | position) >> 1)
         board[row] = 0
         if solution:
               return solution
      return None

   board = [0] * n
   return solve(0, 0, 0, 0)

# Example usage
n = 20  # Change this value to solve for different sizes of the board
solution = solve_n_queens_bitwise(n)

# Convert bit representation to column indices for easier understanding
def bit_to_column(board):
   return [bin(row).count('0') - 1 for row in board]

# Displaying the first few solutions
print(bit_to_column(solution))