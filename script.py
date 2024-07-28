from shatranj.Board import Board
from shatranj.Player import Player
from shatranj.helpers import *

if __name__ == '__main__':
    board = Board( Player( 'Ali', 'white' ), Player( 'Veli', 'black' ) )
    from datetime import datetime
    st = datetime.now()
    res = []
    for i in range( 40000 ):
        res.append( ( board.boardToFEN(), f'{XY2POS( 0, 0 )}{XY2POS( 1, 1 )}' ) )
    print( datetime.now() - st ) 