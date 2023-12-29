def solve_n_queens_no_bitwise(n):
    def solve(row, columns, left_diagonals, right_diagonals):
        if row == n:
            # All queens are placed successfully
            return [col for col in board]

        for col in range(n):
            if col in columns or (row - col) in left_diagonals or (row + col) in right_diagonals:
                # Position is under attack, skip it
                continue

            # Place the queen
            board[row] = col
            columns.add(col)
            left_diagonals.add(row - col)
            right_diagonals.add(row + col)

            # Solve for the next row
            solution = solve(row + 1, columns, left_diagonals, right_diagonals)
            if solution:
                return solution

            # Backtrack
            board[row] = 0
            columns.remove(col)
            left_diagonals.remove(row - col)
            right_diagonals.remove(row + col)

        return None

    board = [0] * n
    return solve(0, set(), set(), set())

# Example usage
n = 28  # Change this value to solve for different sizes of the board
solution_no_bitwise = solve_n_queens_no_bitwise(n)
print(solution_no_bitwise)