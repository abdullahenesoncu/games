
board = [
    [None, None, None],
    [None, None, None],
    [None, None, None],
]

turn = 'x'

def print_board():
    cboard = [ [ c if c else '.' for c in row ] for row in board ]
    print( '  a b c' )
    print( f'3 {cboard[0][0]} {cboard[0][1]} {cboard[0][2]}' )
    print( f'2 {cboard[1][0]} {cboard[1][1]} {cboard[1][2]}' )
    print( f'1 {cboard[2][0]} {cboard[2][1]} {cboard[2][2]}' )

while True:
    print_board()
    win = None

    # Check For Rows
    for i in range(3):
        # Check i. Row
        if board[i][0] is None: continue
        if board[i][0] == board[i][1] == board[i][2]:
            win = board[i][0]
    
    # Check For Columns
    for j in range(3):
        # Check j. Column
        if board[0][j] is None: continue
        if board[0][j] == board[1][j] == board[2][j]:
            win = board[0][j]

    # Check Left Diagonal
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        win = board[0][0]

    #Check Right Diagonal
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        win = board[0][2]

    # Print Winner if Someone Wins
    if win:
        print( f'{win} wins!' )
        break
    
    # Check draw condition, if all cells are filled
    if all( [ c is not None for row in board for c in row ] ):
        print( 'Draw!' )
        break
    
    # Get Input and Validate
    s = input( f'{turn}\'s turn. Please enter your move(like a1, c2): ' )
    if len(s) != 2 or s[0] not in ['a', 'b', 'c'] or s[1] not in ['1', '2', '3']:
        print( 'Invalid move!' )
        continue

    column = ord(s[0]) - ord('a')
    row = 3-int(s[1])

    if board[row][column] is not None:
        print( 'Invalid move!' )
        continue
    
    print( 'Move successful!' )
    board[row][column] = turn
    turn = 'x' if turn == 'o' else 'o'