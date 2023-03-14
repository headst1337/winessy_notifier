from web3 import Web3

from abi.delivery_abi import ABI

from utils.node_rpc import NodeRpc
from utils.config import DELIVERY_ADDRESS, BSC_RPC_URL


class DeliveryContract():

    def __init__(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(NodeRpc.get_new_rpc()))
        self.address = DELIVERY_ADDRESS
        self.abi = ABI
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def get_new_events(self, last_block_number, lost_blocks) -> list:
        events = []
        # event_filter_create = self.contract.events.CreateOrder.createFilter(fromBlock=last_block_number + 1)
        # event_filter_cancel = self.contract.events.CancelOrder.createFilter(fromBlock=last_block_number + 1)
        # event_filter_execute = self.contract.events.ExecuteOrder.createFilter(fromBlock=last_block_number + 1)
        # events.extend(event_filter_create.get_all_entries())
        # events.extend(event_filter_cancel.get_all_entries())
        # events.extend(event_filter_execute.get_all_entries())
        return events
    
    @staticmethod
    def create():
        return DeliveryContract()
