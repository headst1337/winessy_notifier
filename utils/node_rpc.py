from web3 import Web3

from utils.config import BSC_RPC_URL
from utils.rpc_list import RPC_LIST
from utils.logger import Logger


class NodeRpc:
    
    @staticmethod
    def get_new_rpc() -> str:
        logging = Logger("NodeRpcLogger")

        default_rpc = BSC_RPC_URL
        try:
            web3 = Web3(Web3.HTTPProvider(default_rpc))
            if web3.isConnected():
                block_number = web3.eth.block_number
                return default_rpc
        except:
            logging.warning("Default RPC is down. Trying another one...")
            for rpc in RPC_LIST:
                try:
                    web3 = Web3(Web3.HTTPProvider(rpc))
                    if web3.isConnected():
                        block_number = web3.eth.block_number
                        return rpc
                except:
                    pass # he-he 😊
            logging.error("All RPCs are down. Exiting...")
            exit()