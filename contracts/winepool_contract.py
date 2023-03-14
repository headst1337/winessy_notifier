from web3 import Web3
from concurrent.futures import ThreadPoolExecutor
from eth_abi import decode_abi, encode_abi
from eth_utils import function_abi_to_4byte_selector, keccak


from utils.node_rpc import NodeRpc

from contracts.factory_contract import FactoryContract
from utils.event import Event

from abi.winepool_abi import ABI



class WinePoolContract():

    def __init__(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(NodeRpc.get_new_rpc()))
        self.abi = ABI
        self.factory = FactoryContract()

    def get_new_events(self, last_block_number, lost_blocks) -> list:
        print("get_new_events") 
        events = []
        #addresses = self.factory.get_winepools_addresses()
        addresses = ['0x292f87d79F861cB56687F1233fE2aE8ef8881b92']
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.get_events_from_contract, address, last_block_number, lost_blocks, poolid) for poolid, address in enumerate(addresses)]
            for future in futures:
                events.extend(future.result())
        return events
    
    def get_events_from_contract(self, address, last_block_number, lost_blocks, poolid):
        print("get_events_from_contract")

        method_name = 'transferFrom'
        arg_types = ['address', 'address', 'uint256']

        # Получаем 4-байтный селектор метода
        selector = function_abi_to_4byte_selector({'name': method_name, 'inputs': arg_types})

        # Получаем хеш сигнатуры, включая селектор и типы аргументов
        signature_hash = keccak(text=str(selector) + encode_abi(arg_types).hex())

        # Получаем текстовое представление хеша сигнатуры
        signature_hex = '0x' + signature_hash.hex()

        events = []
        filter_params = {
            # 'fromBlock': last_block_number - lost_blocks,
            # 'toBlock': last_block_number,
            'fromBlock': 26325349,
            'toBlock': 26325351,
            'address': address,
            # 'topics': [self.web3.keccak(text='transferFrom(address,address,uint256)').hex()]
            'topics': [signature_hash]
        }
        logs = self.web3.eth.getLogs(filter_params)
        for log in logs:
            tx_hash = log['transactionHash']
            tx_hash_hex = tx_hash.hex()
            tx_receipt = self.web3.eth.getTransactionReceipt(tx_hash_hex)
            decoded_log = decode_abi(['address', 'address', 'uint256'], log['data'])
            from_address = decoded_log[0]
            to_address = decoded_log[1]
            token_id = decoded_log[2]

            event = Event("TransefFrom" ,tx_hash, from_address, to_address, token_id, poolid)
            events.extend(event)
        print(events)
        return events
    
    @staticmethod
    def create():
        return WinePoolContract()


