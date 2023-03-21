import time
import threading

from web3 import Web3

from contracts.base_contract_class import BaseContractClass
from contracts.second_market_contract import SecondMarketContract
from contracts.delivery_contract import DeliveryContract

from utils.config import *
from utils.node_rpc import NodeRpc
from utils.logger import Logger
from utils.request import Request


class WinessyNotifierManager:

    def __init__(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
        self.last_block_number = self.web3.eth.block_number
        self.logging = Logger("ManagerLogger")
        self.request = Request()

    def run(self, func, *args, **kwargs):
        self.logging.info("Starting Winessy Notifier...")
        threading.Thread(target=func, args=args, kwargs=kwargs, name="PollEventsThread").start()

    def _poll_events(self, baseContractClass):
        while True:
            try:
                self._process_new_blocks(baseContractClass)
            except Exception as e:
                self._handle_rpc_error(e, baseContractClass)
            finally:
                time.sleep(5)

    def _process_new_blocks(self, baseContractClass):
        latest_block_number = self.web3.eth.block_number
        if latest_block_number > self.last_block_number:
            lost_blocks = latest_block_number - self.last_block_number
            self.logging.info(f"New block detected: {latest_block_number}")
            self.logging.info(f"Blocks for processing: {lost_blocks}")
            events = baseContractClass.get_new_events(
                latest_block_number, lost_blocks)
            for event in events:
                self._handle_event(event)
            self.last_block_number = latest_block_number

    def _handle_rpc_error(self, error, baseContractClass):
        self.logging.error(f"Error: {error}")
        baseContractClass = BaseContractClass()
        self.web3 = Web3(Web3.HTTPProvider(NodeRpc.get_new_rpc()))
        self.logging.info("Swap on other rpc")

    def _handle_event(self, event):
        event_name = event.event
        event_args = event.args
        txn_hash = event.transactionHash.hex()

        self.logging.info(
            f"New event detected: {event_name}, Args: {event_args}, Transaction hash: {txn_hash}")

        event_map = {
            'CreateOrder': (SecondMarketContract.get_create_order_event_data, 8),
            'CancelOrder': (SecondMarketContract.get_cancel_order_event_data, 9),
            'ExecuteOrder': (SecondMarketContract.get_execute_order_event_data, 10),
            'CreateDeliveryRequest': (DeliveryContract.get_create_delivery_event_data, 11),
            #'SetDeliveryTaskAmount': (DeliveryContract.get_set_delivery_event_data, 12),
            'PayDeliveryTaskAmount': (DeliveryContract.get_pay_delivery_event_data, 13),
            'FinishDeliveryTask': (DeliveryContract.get_finish_delivery_event_data, 14)
        }
        if event_name in event_map:
            event_func, notifier_id = event_map[event_name]
            event_dto, event_class = event_func(event_args)
            self.request.send_post_request(
                event_dto, event_class, txn_hash, notifier_id=notifier_id)
        else:
            self.logging.warning(f"Unsupported event detected: {event_name}")


if __name__ == "__main__":
    swapNode = NodeRpc()
    notifier = WinessyNotifierManager()
    baseContractClass = BaseContractClass()
    notifier.run(notifier._poll_events, baseContractClass)
