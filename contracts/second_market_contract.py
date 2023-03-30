from __future__ import annotations

from web3 import Web3

from abi.second_market_abi import ABI

from utils.node_rpc import NodeRpc
from utils.config import SECOND_MARKET_ADDRESS
from utils.config import CREATE_ORDER_EVENT_CLASS
from utils.config import CANCEL_ORDER_EVENT_CLASS
from utils.config import EXECUTE_ORDER_EVENT_CLASS


class SecondMarketContract():

    def __init__(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(NodeRpc.get_new_rpc()))
        self.address = SECOND_MARKET_ADDRESS
        self.abi = ABI
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def _get_event_entries(self, event, from_block, to_block) -> list:
        event_filter = event.createFilter(fromBlock=from_block, toBlock=to_block)
        return event_filter.get_all_entries()

    def get_new_events(self, last_block_number, lost_blocks) -> list:
        from_block = last_block_number - lost_blocks
        to_block = last_block_number
        event_types = [
            self.contract.events.CreateOrder,
            self.contract.events.CancelOrder,
            self.contract.events.ExecuteOrder,
        ]
        events = [
            event_entry
            for event_type in event_types
            for event_entry in self._get_event_entries(event_type, from_block, to_block)
        ]
        return events
    
    @staticmethod
    def create() -> SecondMarketContract:
        return SecondMarketContract()
    
    @staticmethod
    def get_create_order_event_data(event_args) -> tuple:
        event_dto = {
            "orderId": event_args.orderId,
            "poolId": event_args.poolId,
            "tokenId": event_args.tokenId,
            "seller": event_args.seller,
            "currency": event_args.currency,
            "price": event_args.price
        }
        event_class = CREATE_ORDER_EVENT_CLASS
        return event_dto, event_class

    @staticmethod
    def get_cancel_order_event_data(event_args) -> tuple:
        event_dto = {
            "orderId": event_args.orderId
        }
        event_class = CANCEL_ORDER_EVENT_CLASS
        return event_dto, event_class

    @staticmethod
    def get_execute_order_event_data(event_args) -> tuple:
        event_dto = {
            "orderId": event_args.orderId,
            "buyer": event_args.buyer,
            "orderFee": event_args.orderFee,
            "storageFee": event_args.storageFee
        }
        event_class = EXECUTE_ORDER_EVENT_CLASS
        return event_dto, event_class


