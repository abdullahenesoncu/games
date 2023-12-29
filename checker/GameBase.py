class GameBase:
    @classmethod
    def getInitialRepr( cls ):
        raise NotImplementedError()
    
    @classmethod
    def getScore( cls, repr ):
        raise NotImplementedError()
    
    @classmethod
    def getPossibleMoves( cls, repr ):
        raise NotImplementedError()
    
    @classmethod
    def isGameOver( cls, repr ):
        raise NotImplementedError()
    
    @classmethod
    def winner( cls, repr ):
        raise NotImplementedError()
    
    def play( cls, move ):
        raise NotImplementedError()