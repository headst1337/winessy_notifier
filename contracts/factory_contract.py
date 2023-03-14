from web3 import Web3

from abi.factrory_abi import ABI

from utils.node_rpc import NodeRpc
from utils.config import FACTORY_ADDRESS, BSC_RPC_URL


class FactoryContract():

    def __init__(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(NodeRpc.get_new_rpc()))
        self.address = FACTORY_ADDRESS
        self.abi = ABI
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def get_winepools_addresses(self) -> list:
        return self.contract.functions.getActivePools().call()
