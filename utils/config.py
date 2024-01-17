# Binance Smart Chain node url

BSC_RPC_URL = 'https://polygon-mainnet.g.alchemy.com/v2/M0_ghhKhRygDknTjg5Qs39sEWQod9eRZ'

# Endpoint url

ENDPOINT_URL = 'https://backend.winessy.com/winessy_notifier/protocol_v1/event/new'

# Smart contract adsresses

SECOND_MARKET_ADDRESS = '0xe5B8B57833999719eb07f8e25Fbf82d3Cf2e25E1'
FACTORY_ADDRESS = '0xba15f22FD07d2073EA3CE1f389f487143b4b80d5'
DELIVERY_ADDRESS = '0xfaFCd18d4C295fE9590b9f247C5006Ed512BcE1F'

# Event class

CREATE_ORDER_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeCreateOrder'
CANCEL_ORDER_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeCancelOrder'
EXECUTE_ORDER_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeExecuteOrder'
WINE_POOL_TRANSFER_EVENT_CLASS ='DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WinePoolTransfer'
DELIVERY_CREATE_EVENT_CLASS ='DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineDeliveryServiceCreateDeliveryTask'
DELIVERY_SET_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineDeliveryServiceSetDeliveryTaskAmount'
DELIVERY_PAY_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineDeliveryServicePayDeliveryTaskAmount'
DELIVERY_FINISH_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineDeliveryServiceFinishDeliveryTask'
DELIVERY_CANCEL_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineDeliveryServiceCancelDeliveryTask'
WINE_POOL_MINT_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WinePoolMintToken'