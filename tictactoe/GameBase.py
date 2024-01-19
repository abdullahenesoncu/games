class GameBase:
    @classmethod
    def getInitialRepr(cls):
        raise NotImplementedError()

    @classmethod
    def getScore(cls, repr):
        raise NotImplementedError()

    @classmethod
    def getPossibleMoves(cls, repr):
        raise NotImplementedError()

    @classmethod
    def isGameOver(cls, repr):
        raise NotImplementedError()

    @classmethod
    def winner(cls, repr):
        raise NotImplementedError()
    
    @classmethod
    def rollDice(cls):
        raise NotImplementedError()
    
    @classmethod
    def hasDice(cls):
        return False
    
    def play(self, input, dice=None):
        raise NotImplementedError()