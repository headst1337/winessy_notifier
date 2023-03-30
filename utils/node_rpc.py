from web3 import Web3

from utils.config import BSC_RPC_URL
from utils.rpc_list import RPC_LIST
from utils.logger import Logger


class NodeRpc:
    
    @staticmethod
    def _is_connected(rpc: str, logging) -> bool:
        try:
            web3 = Web3(Web3.HTTPProvider(rpc))
            if web3.isConnected():
                block_number = web3.eth.block_number
                return True
        except Exception as e:
            logging.warning(f"Failed to connect to RPC {rpc}. Reason: {str(e)}")
            return False

        return False

    @staticmethod
    def get_new_rpc() -> str:

        default_rpc_url = BSC_RPC_URL
        rpc_list = RPC_LIST

        logging = Logger("NodeRpcLogger")

        if NodeRpc._is_connected(default_rpc_url, logging):
            return default_rpc_url

        logging.warning("Default RPC is down. Trying another one...")

        for rpc in rpc_list:
            if NodeRpc._is_connected(rpc, logging):
                return rpc

        logging.error("All RPCs are down. Exiting...")
        return None