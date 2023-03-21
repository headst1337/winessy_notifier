

class Event():
    """
    Custom event data class
    """

    def __init__(self, event, transactionHash, src, dst, tokenId, poolId):
        self.event = event
        self.transactionHash = transactionHash
        self.dst = dst
        self.src = src
        self.tokenId = tokenId
        self.poolId = poolId