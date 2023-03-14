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

    def get_new_events(self, last_block_number, lost_blocks) -> list:
        events = []
        event_filter_create = self.contract.events.CreateOrder.createFilter(fromBlock=last_block_number - lost_blocks, toBlock=last_block_number)
        event_filter_cancel = self.contract.events.CancelOrder.createFilter(fromBlock=last_block_number - lost_blocks, toBlock=last_block_number)
        event_filter_execute = self.contract.events.ExecuteOrder.createFilter(fromBlock=last_block_number - lost_blocks, toBlock=last_block_number)
        events.extend(event_filter_create.get_all_entries())
        events.extend(event_filter_cancel.get_all_entries())
        events.extend(event_filter_execute.get_all_entries())
        return events
    
    @staticmethod
    def create():
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


