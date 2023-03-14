

class Event():
    """
    Custom event data class
    """

    def __init__(self, event, tx_hash, from_address, to_address, token_id, poolid):
        self.event = event
        self.tx_hash = tx_hash
        self.from_address = from_address
        self.to_address = to_address
        self.token_id = token_id
        self.poolid = poolid