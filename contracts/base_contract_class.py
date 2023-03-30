from contracts.delivery_contract import DeliveryContract
from contracts.second_market_contract import SecondMarketContract
from contracts.winepool_contract import WinePoolContract


class BaseContractClass:

    def __init__(self) -> None:
        self.contracts = [
            DeliveryContract.create(),
            SecondMarketContract.create(),
            #WinePoolContract.create(),
        ]

    def get_new_events(self, param, lost_blocks) -> list:
        events = []
        for contract in self.contracts:
            events.extend(contract.get_new_events(param, lost_blocks))
        return events
