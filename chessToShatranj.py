import sys

parts = sys.argv[ 1 : ]
parts[ 0 ] = parts[ 0 ].replace( 'n', 'h' ).replace( 'b', 'f' ).replace( 'k', 's' ).replace( 'q', 'v' )
parts[ 0 ] = parts[ 0 ].replace( 'N', 'H' ).replace( 'B', 'F' ).replace( 'K', 'S' ).replace( 'Q', 'V' )

print( parts[ 0 ], parts[ 1 ], parts[ 4 ], parts[ 5 ] )