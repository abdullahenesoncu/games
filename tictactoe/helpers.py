def XY2POS( x, y ):
    return f'{chr(ord("a")+x)}{y+1}'
def POS2XY( pos ):
    return ord( pos[0].lower() ) - ord( 'a' ), int( pos[1] ) - 1