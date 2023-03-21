from web3 import Web3

from abi.delivery_abi import ABI

from utils.node_rpc import NodeRpc
from utils.config import DELIVERY_ADDRESS
from utils.config import DELIVERY_CREATE_EVENT_CLASS
from utils.config import DELIVERY_SET_EVENT_CLASS
from utils.config import DELIVERY_CREATE_EVENT_CLASS
from utils.config import DELIVERY_PAY_EVENT_CLASS
from utils.config import DELIVERY_FINISH_EVENT_CLASS


class DeliveryContract():

    def __init__(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(NodeRpc.get_new_rpc()))
        self.address = DELIVERY_ADDRESS
        self.abi = ABI
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def get_new_events(self, last_block_number, lost_blocks) -> list:
        events = []
        event_filter_create = self.contract.events.CreateDeliveryRequest.createFilter(fromBlock=last_block_number - lost_blocks, toBlock=last_block_number)
        #event_filter_set = self.contract.events.SetDeliveryTaskAmount.createFilter(fromBlock=last_block_number - lost_blocks, toBlock=last_block_number)
        event_filter_pay = self.contract.events.PayDeliveryTaskAmount.createFilter(fromBlock=last_block_number - lost_blocks, toBlock=last_block_number)
        event_filter_finish = self.contract.events.FinishDeliveryTask.createFilter(fromBlock=last_block_number - lost_blocks, toBlock=last_block_number)
        events.extend(event_filter_create.get_all_entries())
        #events.extend(event_filter_set.get_all_entries())
        events.extend(event_filter_pay.get_all_entries())
        events.extend(event_filter_finish.get_all_entries())
        return events
    
    @staticmethod
    def create():
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
    
    # @staticmethod
    # def get_set_delivery_event_data(event_args) -> tuple:
    #     event_dto = {
    #         "deliveryTaskId": event_args.deliveryTaskId,
    #         "poolId": event_args.poolId,
    #         "tokenId": event_args.tokenId,
    #         "amount": event_args.amount,
    #         "bcbAmount": event_args.bcbAmount
    #     }
    #     event_class = DELIVERY_SET_EVENT_CLASS
    #     return event_dto, event_class
    
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
