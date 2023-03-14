from contracts.delivery_contract import DeliveryContract
from contracts.second_market_contract import SecondMarketContract
from contracts.winepool_contract import WinePoolContract


class BaseContractClass():
    def __init__(self):
        # Создаем экземпляры каждого дочернего класса
        self.delivery_contract = DeliveryContract.create()
        self.second_market_contract = SecondMarketContract.create()
        #self.wine_pool_contract = WinePoolContract.create()

    def get_new_events(self, param, lost_blocks):
        events = []
        events.extend(self.delivery_contract.get_new_events(param, lost_blocks))
        events.extend(self.second_market_contract.get_new_events(param, lost_blocks))
        #events.extend(self.wine_pool_contract.get_new_events(param, lost_blocks))
        return events
