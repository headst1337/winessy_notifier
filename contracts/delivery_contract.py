from __future__ import annotations

from web3 import Web3

from abi.delivery_abi import ABI

from utils.node_rpc import NodeRpc
from utils.config import DELIVERY_ADDRESS
from utils.config import DELIVERY_CREATE_EVENT_CLASS
from utils.config import DELIVERY_CREATE_EVENT_CLASS
from utils.config import DELIVERY_PAY_EVENT_CLASS
from utils.config import DELIVERY_FINISH_EVENT_CLASS


class DeliveryContract():

    def __init__(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(NodeRpc.get_new_rpc()))
        self.address = DELIVERY_ADDRESS
        self.abi = ABI
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def _get_event_entries(self, event, from_block, to_block) -> list:
        event_filter = event.createFilter(fromBlock=from_block, toBlock=to_block)
        return event_filter.get_all_entries()

    def get_new_events(self, last_block_number, lost_blocks) -> list:
        from_block = last_block_number - lost_blocks
        to_block = last_block_number
        event_types = [
            self.contract.events.CreateDeliveryRequest,
            self.contract.events.PayDeliveryTaskAmount,
            self.contract.events.FinishDeliveryTask,
            self.contract.events.CancelDeliveryTask,
        ]
        events = [
            event_entry
            for event_type in event_types
            for event_entry in self._get_event_entries(event_type, from_block, to_block)
        ]
        return events
    
    @staticmethod
    def create() -> DeliveryContract:
        return DeliveryContract()
    
    @staticmethod
    def get_create_delivery_event_data(event_args) -> tuple:
        event_dto = {
                "deliveryTaskId": event_args.deliveryTaskId,
				"poolId": event_args.poolId,
				"tokenId": event_args.tokenId,
				"tokenOwner": event_args.tokenOwner,
				"isInternal": event_args.isInternal
            }
        event_class = DELIVERY_CREATE_EVENT_CLASS
        return event_dto, event_class
    
    @staticmethod
    def get_pay_delivery_event_data(event_args) -> tuple:
        event_dto = {
            "deliveryTaskId": event_args.deliveryTaskId,
            "poolId": event_args.poolId,
            "tokenId": event_args.tokenId,
            "tokenOwner": event_args.tokenOwner,
            "isInternal": event_args.isInternal,
            "amount": event_args.amount,
            "bcbAmount": event_args.bcbAmount
        }
        event_class = DELIVERY_PAY_EVENT_CLASS
        return event_dto, event_class
    
    @staticmethod
    def get_finish_delivery_event_data(event_args) -> tuple:
        event_dto = {
            "deliveryTaskId": event_args.deliveryTaskId,
            "poolId": event_args.poolId,
            "tokenId": event_args.tokenId
        }
        event_class = DELIVERY_FINISH_EVENT_CLASS
        return event_dto, event_class
    
    @staticmethod
    def get_cancel_delivery_event_data(event_args) -> tuple:
        event_dto = {
            "deliveryTaskId": event_args.deliveryTaskId,
            "poolId": event_args.poolId,
            "tokenId": event_args.tokenId
        }
        event_class = DELIVERY_FINISH_EVENT_CLASS
        return event_dto, event_class
