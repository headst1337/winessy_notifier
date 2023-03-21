import time
import requests
import uuid

from utils.config import ENDPOINT_URL
from utils.logger import Logger


class Request:
    def __init__(self) -> None:
        self.logging = Logger("RequestLogger")

    def send_post_request(self, concrete_event_dto, event_class, txn_hash, notifier_id):
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
                    "node_creation_time": int(time.time()),
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
        HEADERS = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
            
        #self.logging.info('Test send!')
        response = requests.post(ENDPOINT_URL, headers=HEADERS, json=data)

        try:
            response.raise_for_status()
            self.logging.info('Successful!')
        except requests.exceptions.HTTPError as e:
            self.logging.error(f'Failed! Status code: {response.status_code}. Error: {e}')

