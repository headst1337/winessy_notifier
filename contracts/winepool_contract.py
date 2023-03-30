# from __future__ import annotations

# from web3 import Web3
# from web3.middleware import geth_poa_middleware
# from eth_abi import decode_abi

# from abi.winepool_abi import ABI

# from utils.node_rpc import NodeRpc
# from utils.event import Event
# from utils.config import WINE_POOL_TRANSFER_EVENT_CLASS
# from contracts.factory_contract import FactoryContract


class WinePoolContract():

    def __init__(self) -> None:
        pass
        # self.web3 = Web3(Web3.HTTPProvider(NodeRpc.get_new_rpc()))
        # self.abi = ABI
        # self.factory = FactoryContract()

    # def get_new_events(self, last_block_number, lost_blocks) -> list:
    #     events = []
    #     return events
                        
    # @staticmethod
    # def create() -> WinePoolContract:
    #     return WinePoolContract()

    # @staticmethod
    # def get_tranfer_from_order_data(event_args) -> tuple:
    #     event_dto = {
    #         "poolId": event_args.poolId,
    #         "tokenId": event_args.tokenId,
    #         "from": event_args.src,
    #         "to": event_args.dst
    #     }
    #     event_class = WINE_POOL_TRANSFER_EVENT_CLASS
    #     return event_dto, event_class


