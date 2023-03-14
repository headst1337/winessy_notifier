import datetime
import time
import threading
import uuid
import logging

import requests

from web3 import Web3

from contracts.base_contract_class import BaseContractClass

from utils.config import *
from utils.node_rpc import NodeRpc

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


class WinessyNotifierManager:

    def __init__(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
        print(self.web3.clientVersion)
        self.last_block_number = self.web3.eth.block_number

    def run(self, func):
        logging.info("Starting Winessy Notifier...")
        threading.Thread(target=func).start()

    def _poll_events(self, baseContractClass):
        while True:
            try:
                latest_block_number = self.web3.eth.block_number
                if latest_block_number > self.last_block_number:
                    lost_blocks = latest_block_number - self.last_block_number
                    logging.info(f"New block detected: {latest_block_number}")
                    logging.info(f"Blocks for processing: {lost_blocks}")
                    events = baseContractClass.get_new_events(latest_block_number, lost_blocks)
                    for event in events:
                        self._handle_event(event)
                    self.last_block_number = latest_block_number
            except Exception as e:
                logging.error(f"Error: {e}")
                baseContractClass = BaseContractClass()
                self.web3 = Web3(Web3.HTTPProvider(NodeRpc.get_new_rpc()))
            finally:
                # Wait for some time before checking for new events again
                time.sleep(10)

    def _handle_event(self, event):
        print("_handle_event")
        event_name = event.event
        event_args = event.args
        txn_hash = event.transactionHash.hex()

        logging.info(f"New event detected: {event_name}, Args: {event_args}, Transaction hash: {txn_hash}")

        if event_name == 'CreateOrder':
            concrete_event_dto = {
                "orderId": event_args.orderId,
                "poolId": event_args.poolId,
                "tokenId": event_args.tokenId,
                "seller": event_args.seller,
                "currency": event_args.currency,
                "price": event_args.price
            }
            event_class = CREATE_ORDER_EVENT_CLASS
            self._send_post_request(concrete_event_dto, event_class, txn_hash, notifier_id=8)

        elif event_name == 'CancelOrder':
            concrete_event_dto = {
                "orderId": event_args.orderId
            }
            event_class = CANCEL_ORDER_EVENT_CLASS
            self._send_post_request(concrete_event_dto, event_class, txn_hash, notifier_id=9)

        elif event_name == 'ExecuteOrder':
            concrete_event_dto = {
                "orderId": event_args.orderId,
                "buyer": event_args.buyer,
                "orderFee": event_args.orderFee,
                "storageFee": event_args.storageFee
            }
            event_class = EXECUTE_ORDER_EVENT_CLASS
            self._send_post_request(concrete_event_dto, event_class, txn_hash, notifier_id=10)

        elif event_name == 'TransferFrom':
            concrete_event_dto = {
                "poolId": '?????????????????',
				"tokenId": event_args.amount,
				"from": event_args.src,
				"to": event_args.dst
            }
            event_class = WINE_POOL_TRANSFER_EVENT_CLASS
            self._send_post_request(concrete_event_dto, event_class, txn_hash, notifier_id=4)

        # elif event_name == 'PayDelivery':
        #     concrete_event_dto = {
        #         "?": '?',
        #     }
        #     event_class = DELIVERY_PAY_EVENT_CLASS
        #     self._send_post_request(concrete_event_dto, event_class, txn_hash, notifier_id=11)
        else:
            logging.warning(f"Unsupported event detected: {event_name}")

    def _send_post_request(self, concrete_event_dto, event_class, txn_hash, notifier_id):
        data = {
            "protocol_version": 1,
            "uniq_id": str(uuid.uuid4()),
            "router_information": {
                "service_name": "WinessyMonolith",
                "service_type": "WinessyMonolith",
                "version": "1.0.0",
                "route": "/winessy_notifier/protocol_v1/event/new"
            },
            "permission_checker_information": {
                "service_type": "CryptoTradingMonolith"
            },
            "self_service_information": {
                "service_name": "WinessyNotifier",
                "service_type": "WinessyNotifier",
                "version": "1.0.0",
                "self_address": "http:/nginx-microservice-winessy_notifier",
                "self_uniq_id": "winessy_notifier"
            },
            "data_information": {
                "dto": {
                    "notifier_id": notifier_id,
                    "chain_id": 56,
                    "transaction_hash": txn_hash,
                    "node_creation_time": int(datetime.datetime.now().timestamp()),
                    "_token_tc": "пока отключено",
                    "_method": "пока отключено",
                    "concrete_event": {
                        "dto": concrete_event_dto,
                        "class": event_class
                    }
                },
                "class": "DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\CreateEvent"
            }
        }
        headers = {'Accept': 'application/json',
                'Content-Type': 'application/json'}
        # response = requests.post(ENDPOINT_URL, headers=headers, json=data)

        # if response.ok:
        #     logging.info('Successful!')
        # else:
        #     logging.error(f'Failed! Status code: {response.status_code}')


if __name__ == "__main__":
    notifier = WinessyNotifierManager()
    baseContractClass = BaseContractClass()
    notifier.run(lambda: notifier._poll_events(baseContractClass))
