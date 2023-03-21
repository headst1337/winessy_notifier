from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_abi import decode_abi

from abi.winepool_abi import ABI

from utils.node_rpc import NodeRpc
from utils.event import Event
from utils.config import WINE_POOL_TRANSFER_EVENT_CLASS
from contracts.factory_contract import FactoryContract


class WinePoolContract():

    def __init__(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(NodeRpc.get_new_rpc()))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.abi = ABI
        self.factory = FactoryContract()
        self.transfer_from_signature = ['address', 'address', 'uint256']
        #self.method_id = b'\x23\xb8\x72\xdd'
        self.method_id = "0x23b872dd"

    def get_new_events(self, last_block_number, lost_blocks) -> list:
        events = []
        winePoolsAddressesList = self.factory.get_winepools_addresses()

        for i, winePoolAddress in enumerate(winePoolsAddressesList):
            #for block_num in range(last_block_number - lost_blocks, last_block_number):
            for block_num in range(26325350, 26325350 + 1):
                block = self.web3.eth.getBlock(block_num, full_transactions=True)
                for tx in block.transactions:
                    if tx.to == winePoolAddress and tx.input.startswith(self.method_id):
                    #if True:
                        input_data = tx.input[len(self.method_id):]
                        poolId = i
                        src, dst, tokenId = decode_abi(self.transfer_from_signature, bytes.fromhex(input_data))
                        tx.hash = tx.hash
                        event = Event('TransferFrom', tx.hash, src, dst, tokenId, poolId)
                        events.append(event)
        return events
                        
    @staticmethod
    def create():
        return WinePoolContract()

    @staticmethod
    def get_tranfer_from_order_data(event_args) -> tuple:
        event_dto = {
            "poolId": event_args.poolId,
            "tokenId": event_args.tokenId,
            "from": event_args.src,
            "to": event_args.dst
        }
        event_class = WINE_POOL_TRANSFER_EVENT_CLASS
        return event_dto, event_class


