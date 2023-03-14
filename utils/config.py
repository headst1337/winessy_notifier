BSC_RPC_URL = 'https://1rpc.io/bnb'

#https://1rpc.io/bnb
#https://bsc-dataseed3.binance.org	

ENDPOINT_URL = 'https://backend.winessy.com/winessy_notifier/protocol_v1/event/new'

SECOND_MARKET_ADDRESS = '0x009102b6316A57de021Ee72D561A773432d11D26'
FACTORY_ADDRESS = '0xaDA9B077C5b780C802DdfECB79F859e7cE2a1A69'
DELIVERY_ADDRESS = '0xd621635639e1955a1A92BF6Ff39b536B80600834'

CREATE_ORDER_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeCreateOrder'
CANCEL_ORDER_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeCancelOrder'
EXECUTE_ORDER_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeExecuteOrder'
WINE_POOL_TRANSFER_EVENT_CLASS ='DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WinePoolTransfer'
DELIVERY_CREATE_EVENT_CLASS ='DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineDeliveryServiceCreateDeliveryTask'
DELIVERY_SET_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineDeliveryServiceSetDeliveryTaskAmount'
DELIVERY_PAY_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineDeliveryServicePayDeliveryTaskAmount'
DELIVERY_FINISH_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineDeliveryServiceFinishDeliveryTask'