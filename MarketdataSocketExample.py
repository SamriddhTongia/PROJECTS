from datetime import datetime, timezone
import threading
from Connect import XTSConnect
from MarketDataSocketClient_Ad import MDSocket_io
import json
import pytz

# MarketData API Credentials
API_KEY = "6b8685d40d6971211110b7"
API_SECRET = "Rqle261#Az"
source = "WEBAPI"

# Initialise
# while True:

xt = XTSConnect(API_KEY, API_SECRET, source)
# Login for authorization token
response = xt.marketdata_login()
print(response)

# Store the token and userid
set_marketDataToken = response['result']['token']
set_muserID = response['result']['userID']
print("Login: ", response)
#
# # Connecting to Marketdata socket
soc = MDSocket_io(set_marketDataToken, set_muserID)
#
# # Instruments for subscribing
Instruments = [
                {'exchangeSegment': 1, 'exchangeInstrumentID': 2885}
               ]
#
# # Callback for connection
timezone = pytz.timezone('Asia/Kolkata')
LIVE_FEED_JSON = {}

def on_connect():
    """Connect from the socket."""
    print('Market Data Socket connected successfully!')
#
#     # # Subscribe to instruments
    print('Sending subscription request for Instruments - \n' + str(Instruments))
    response = xt.send_subscription(Instruments, 1501)
    print('Sent Subscription request!')
    print("Subscription response: ", response)

# # Callback on receiving message
def on_message(data):
    print('I received a message!')

# Callback for message code 1501 FULL
def on_message1501_json_full(data):
    data = json.loads(data)
    # print("This is type of", json.loads(data)["ExchangeTimeStamp"])
    # print(datetime.fromtimestamp(data["ExchangeTimeStamp"]))
    # print('I received a 1501 Touchline message!' + str(data))
    LIVE_FEED_JSON[data["ExchangeInstrumentID"]] = {
        "exchng_time": datetime.fromtimestamp(data["ExchangeTimeStamp"], tz=timezone),
        "last_traded_time": data['Touchline']["LastTradedPrice"],
        "bid_price": data['Touchline']['BidInfo']["Price"],
        "ask_price": data['Touchline']['AskInfo']["Price"],
        "temp_time": data['ExchangeTimeStamp']
    }

# Callback for message code 1502 FULL
def on_message1502_json_full(data):
    print(json.loads(data))
    print('I received a 1502 Market depth message!' + data)

# Callback for message code 1505 FULL
def on_message1505_json_full(data):
    print('I received a 1505 Candle data message!' + data)

# Callback for message code 1507 FULL
def on_message1507_json_full(data):
    print('I received a 1507 MarketStatus data message!' + data)

# Callback for message code 1510 FULL
def on_message1510_json_full(data):
    print('I received a 1510 Open interest message!' + data)

# Callback for message code 1512 FULL
def on_message1512_json_full(data):
    print('I received a 1512 Level1,LTP message!' + data)

# Callback for message code 1105 FULL
def on_message1105_json_full(data):
    print('I received a 1105, Instrument Property Change Event message!' + data)


# Callback for message code 1501 PARTIAL
def on_message1501_json_partial(data):
    print('I received a 1501, Touchline Event message!' + data)

# Callback for message code 1502 PARTIAL
def on_message1502_json_partial(data):
    print('I received a 1502 Market depth message!' + data)

# Callback for message code 1505 PARTIAL
def on_message1505_json_partial(data):
    print('I received a 1505 Candle data message!' + data)

# Callback for message code 1510 PARTIAL
def on_message1510_json_partial(data):
    print('I received a 1510 Open interest message!' + data)

# Callback for message code 1512 PARTIAL
def on_message1512_json_partial(data):
    print('I received a 1512, LTP Event message!' + data)



# Callback for message code 1105 PARTIAL
def on_message1105_json_partial(data):
    print('I received a 1105, Instrument Property Change Event message!' + data)

# Callback for disconnection
def on_disconnect():
    print('Market Data Socket disconnected!')


# Callback for error
def on_error(data):
    """Error from the socket."""
    print('Market Data Error', data)


# Assign the callbacks.
soc.on_connect = on_connect
soc.on_message = on_message
soc.on_message1502_json_full = on_message1502_json_full
soc.on_message1505_json_full = on_message1505_json_full
soc.on_message1507_json_full = on_message1507_json_full
soc.on_message1510_json_full = on_message1510_json_full
soc.on_message1501_json_full = on_message1501_json_full
soc.on_message1512_json_full = on_message1512_json_full
soc.on_message1105_json_full = on_message1105_json_full
soc.on_message1502_json_partial = on_message1502_json_partial
soc.on_message1505_json_partial = on_message1505_json_partial
soc.on_message1510_json_partial = on_message1510_json_partial
soc.on_message1501_json_partial = on_message1501_json_partial
soc.on_message1512_json_partial = on_message1512_json_partial
soc.on_message1105_json_partial = on_message1105_json_partial
soc.on_disconnect = on_disconnect
soc.on_error = on_error


# Event listener
el = soc.get_emitter()
el.on('connect', on_connect)
el.on('1501-json-full', on_message1501_json_full)
el.on('1502-json-full', on_message1502_json_full)
el.on('1507-json-full', on_message1507_json_full)
el.on('1512-json-full', on_message1512_json_full)
el.on('1105-json-full', on_message1105_json_full)

# Infinite loop on the main thread. Nothing after this will run.

# {"MessageCode":1501,"MessageVersion":4,"ApplicationType":0,"TokenID":0,"ExchangeSegment":1,"ExchangeInstrumentID":2885,
        # "ExchangeTimeStamp":1362224318,"BookType":1,"XMarketType":1,"SequenceNumber":999069560731610,
# "Touchline":{"LastTradedPrice":2339.85,"LastTradedQunatity":8,"TotalBuyQuantity":287342,"TotalSellQuantity":338997,"TotalTradedQuantity":1954290,
# "AverageTradedPrice":2337.58,"LastTradedTime":1362224318,"LastUpdateTime":1362224318,"PercentChange":-0.17278894150773993,"Open":2337,
# "High":2351.65,"Low":2328.05,"Close":2343.9,"TotalValueTraded":null,"BuyBackTotalBuy":0,"BuyBackTotalSell":0,
# "AskInfo":{"Size":242,"Price":2339.9,"TotalOrders":3,"BuyBackMarketMaker":0},"BidInfo":{"Size":51,"Price":2339.85,
# "TotalOrders":6,"BuyBackMarketMaker":0}}}
# You have to use the pre-defined callbacks to manage subscriptions.
threading.Thread(target=soc.connect).start()
# soc.connect()
print("CURSOR RELEASED")
while True:
    # print(LIVE_FEED_JSON['temp_time'])
    print(LIVE_FEED_JSON)

