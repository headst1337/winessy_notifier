import datetime
import time
import threading
import uuid
import logging

import requests

from web3 import Web3

from abi import ABI
from config import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

class WinessySecondMarketNotifier:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
        self.contract_address = CONTRACT_ADDRESS
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=ABI)
        self.last_block_number = self.w3.eth.block_number

    def run(self):
        logging.info("Starting Winessy Second Market Notifier...")
        threading.Thread(target=self._poll_events).start()

    def _poll_events(self):
        while True:
            try:
                latest_block_number = self.w3.eth.block_number
                if latest_block_number > self.last_block_number:
                    logging.info(f"New block detected: {latest_block_number}")
                    events = self._get_new_events()
                    for event in events:
                        self._handle_event(event)
                    self.last_block_number = latest_block_number
            except Exception as e:
                logging.error(f"Error while polling events: {e}")
            finally:
                # Wait for some time before checking for new events again
                time.sleep(10)

    def _get_new_events(self):
        events = []
        event_filter_create = self.contract.events.CreateOrder.createFilter(fromBlock=self.last_block_number + 1)
        event_filter_cancel = self.contract.events.CancelOrder.createFilter(fromBlock=self.last_block_number + 1)
        event_filter_execute = self.contract.events.ExecuteOrder.createFilter(fromBlock=self.last_block_number + 1)
        events.extend(event_filter_create.get_all_entries())
        events.extend(event_filter_cancel.get_all_entries())
        events.extend(event_filter_execute.get_all_entries())
        return events

    def _handle_event(self, event):
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
            concrete_event_dto = {"orderId": event_args.orderId}
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
        # Отправить POST-запрос с требуемыми заголовками
        headers = {'Accept': 'application/json',
                'Content-Type': 'application/json'}
        response = requests.post(ENDPOINT_URL, headers=headers, json=data)

        # Проверить ответ сервера
        if response.ok:
            logging.info('POST request successful!')
        else:
            logging.error(f'POST request failed! Status code: {response.status_code}')

if __name__ == "__main__":
    notifier = WinessySecondMarketNotifier()
    notifier.run()
