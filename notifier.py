import datetime
import uuid
import requests
from web3 import Web3
import abi
import json

# Устанавливаем соединение с BSC сетью
from web3 import Web3


def createOrder(event_args, txn_hash):

    concrete_event_dto = {
        "orderId": event_args.orderId,
        "poolId": event_args.poolId,
        "tokenId": event_args.tokenId,
        "seller": event_args.seller,
        "currency": event_args.currency,
        "price": event_args.price
    }
    event_class = "DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeCreateOrder"
    sendPostRequest(concrete_event_dto, event_class, txn_hash, notifier_id=8)


def cancelOrder(event_args, txn_hash):
    concrete_event_dto = {"orderId": event_args.orderId}
    event_class = "DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeCancelOrder"
    sendPostRequest(concrete_event_dto, event_class, txn_hash, notifier_id=9)


def excuteOrder(event_args, txn_hash):

    concrete_event_dto = {
        "orderId": event_args.orderId,
        "buyer": event_args.buyer,
        "orderFee": event_args.orderFee,
        "storageFee": event_args.storageFee
    }
    event_class = "DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeExecuteOrder"
    sendPostRequest(concrete_event_dto, event_class, txn_hash, notifier_id=8)


def sendPostRequest(concrete_event_dto, event_class, txn_hash, notifier_id):
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
    url = 'https://backend.winessy.com/winessy_notifier/protocol_v1/event/new'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data)

    # Проверить ответ сервера
    if response.ok:
        print('POST request successful!')
    else:
        print('POST request failed! Status code:', response.status_code)


w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
contract_address = '0x009102b6316A57de021Ee72D561A773432d11D26'
contract = w3.eth.contract(address=contract_address, abi=abi.abi)


while True:
    event_filter_create = contract.events.CreateOrder.createFilter(
        fromBlock='latest')
    event_filter_cancel = contract.events.CancelOrder.createFilter(
        fromBlock='latest')
    event_filter_execute = contract.events.ExecuteOrder.createFilter(
        fromBlock='latest')

    for event in event_filter_create.get_new_entries():
        print(event['event'], event['args'], event.transactionHash.hex())
        if event['event'] == 'CreateOrder':
            createOrder(event['args'], event.transactionHash.hex())

    for event in event_filter_cancel.get_new_entries():
        print(event['event'], event['args'], event.transactionHash.hex())
        if event['event'] == 'CancelOrder':
            cancelOrder(event['args'], event.transactionHash.hex())
            pass

    for event in event_filter_execute.get_new_entries():
        print(event['event'], event['args'], event.transactionHash.hex())
        if event['event'] == 'ExecuteOrder':
            excuteOrder(event['args'], event.transactionHash.hex())
            pass
