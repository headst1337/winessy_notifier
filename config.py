BSC_RPC_URL = 'https://bsc-dataseed1.binance.org:443'

ENDPOINT_URL = 'https://backend.winessy.com/winessy_notifier/protocol_v1/event/new'

CONTRACT_ADDRESS = '0x009102b6316A57de021Ee72D561A773432d11D26'

CREATE_ORDER_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeCreateOrder'
CANCEL_ORDER_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeCancelOrder'
EXECUTE_ORDER_EVENT_CLASS = 'DTO\\WinessyNotifier\\Version1\\NotifierNotification\\Request\\ConcreteEvent\\WineMarketPlaceCodeExecuteOrder'