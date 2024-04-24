from time import sleep
from datetime import datetime, time,timedelta
import threading
from Connect import XTSConnect
from MarketDataSocketClient_Ad import MDSocket_io
import json
from main import *
from main_functions import *
from pymongo import MongoClient
from main_interactive import BUY,SELL


# # Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017')

# # Access or create a database
# db = client['mydatabase']

# # Access or create a collection
# collection = db['mycollection']


# Marketdata API Credentials
API_KEY = "88a85e1ab0e12049bdf453"
API_SECRET = "Dsti357$at"
XTS_API_BASE_URL = "https://xts-api.trading"
source = "WEBAPI"

xt = XTSConnect(API_KEY, API_SECRET, source)
# Login for authorization token
response = xt.marketdata_login()
print(response)

# Store the token and userid
set_marketDataToken = response['result']['token']
set_muserID = response['result']['userID']
print("Login: ", response)

soc = MDSocket_io(set_marketDataToken, set_muserID)

# tokens = token_generator(strikes_bnf(xt))
print(FINAL_INSTRUMENTS)
LIVE_FEED_JSON = {}


def on_connect():
    """Connect from the socket."""
    print('Market Data Socket connected successfully!')
    #
    #     # # Subscribe to instruments
    print('Sending subscription request for Instruments - \n' + str(FINAL_INSTRUMENTS))
    response = xt.send_subscription(FINAL_INSTRUMENTS, 1512)
    print('Sent Subscription request!')
    print("Subscription response: ", response)


# # Callback on receiving message
def on_message(data):
    print('I received a message!')


# Callback for message code 1501 FULL
def on_message1501_json_full(data):
    data = json.loads(data)
    # print(data)
    # print("data is", data)
    # print("This is type of", json.loads(data)["ExchangeTimeStamp"])
    # print(datetime.fromtimestamp(data["ExchangeTimeStamp"]))
    # print('I received a 1501 Touchline message!' + str(data))

    # LIVE_FEED_JSON[data["ExchangeInstrumentID"]] = {    # Yahaa se
    #     "exchng_time": datetime.utcfromtimestamp(data['ExchangeTimeStamp']).strftime('%Y-%m-%d %H:%M:%S'),
    #     "last_traded_time": data['Touchline']["LastTradedPrice"],
    #     "bid_price": data['Touchline']['BidInfo']["Price"],
    #     "ask_price": data['Touchline']['AskInfo']["Price"],
    # }

    # print(LIVE_FEED_JSON)


# Callback for message code 1502 FULL
def on_message1502_json_full(data):
    print(json.loads(data))
    print('I received a 1502 Market depth message!' + data)


# Callback for message code 1505 FULL
def on_message1505_json_full(data):
    print('I received a 1505 Candle data message!' + data)


# Callback for message code 1507 FULL
def on_message1507_json_full(data):
    print('I received a 1507 MarketStatus data message!' +str(data))


# Callback for message code 1510 FULL
def on_message1510_json_full(data):
    print('I received a 1510 Open interest message!' + data)


# Callback for message code 1512 FULL
def on_message1512_json_full(data):
    data = json.loads(data)
    LIVE_FEED_JSON[data["ExchangeInstrumentID"]] = data['LastTradedPrice']
    # store_values_in_db(LIVE_FEED_JSON)
    # print(data)
    # print("data is", data["ExchangeInstrumentID"], "Last Traded Price", data['LastTradedPrice'])

    # print('I received a 1512 Level1,LTP message!' + data) #changed

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

# soc.connect()
threading.Thread(target=soc.connect).start()
data=LIVE_FEED_JSON
quantity={'NIFTY':50*LOT_SIZE_NIFTY,'BANKNIFTY':15*LOT_SIZE_BANKNIFTY,'FINNIFTY':40*LOT_SIZE_FINNIFTY}
while True:
    if len(LIVE_FEED_JSON)<len(FINAL_INSTRUMENT_ID):
        continue

    for i in range(len(FINAL_INSTRUMENT_ID)):
        current_time = datetime.now().time()

        if (time_start_input <= current_time) & (current_time <= dt.time(time_stop_input.hour,time_stop_input.minute+5)):

            # current_price=data[FINAL_INSTRUMENT_ID[i]]
            current_price=2

            if (current_price>= FINAL_PREMIUM[i] * 2) and (FINAL_POSITION[i]==0):
                FINAL_POSITION[i]=1
                update_in_initial_doc(FINAL_INSTRUMENT_ID[i],FINAL_INDEX[i],'buy_price',current_price)
                store_signal(FINAL_INDEX[i],FINAL_PREMIUM[i],1,current_price,FINAL_STRIKE[i],search_in_initial_doc(FINAL_INSTRUMENT_ID[i],FINAL_INDEX[i],'option_type'),FINAL_INSTRUMENT_ID[i],FINAL_EXPIRY[i],quantity[FINAL_INDEX[i]])
                update_in_initial_doc(FINAL_INSTRUMENT_ID[i],FINAL_INDEX[i],'position',1)
                BUY(EXCHANGE_ID=FINAL_INSTRUMENT_ID[i],QUANTITY=quantity[FINAL_INDEX[i]])

            if FINAL_POSITION[i]==1 and search_in_transaction_doc(FINAL_INSTRUMENT_ID[i],FINAL_INDEX[i],'signal')==1:

                buy_price=search_in_initial_doc(FINAL_INSTRUMENT_ID[i],FINAL_INDEX[i],'buy_price')
                x=(buy_price)*calculate_stop_loss(FINAL_PREMIUM[i])
                if current_price<=x :

                    FINAL_POSITION[i]=-1
                    update_in_initial_doc(FINAL_INSTRUMENT_ID[i],FINAL_INDEX[i],'sell_price',current_price)
                    update_in_transaction_doc(FINAL_INSTRUMENT_ID[i],'sell_price',current_price)
                    update_in_transaction_doc(FINAL_INSTRUMENT_ID[i],'timestamp_sell',datetime.now())
                    update_in_transaction_doc(FINAL_INSTRUMENT_ID[i],'signal',-1)
                    update_in_initial_doc(FINAL_INSTRUMENT_ID[i],FINAL_INDEX[i],'position',-1)
                    SELL(EXCHANGE_ID=FINAL_INSTRUMENT_ID[i],QUANTITY=quantity[FINAL_INDEX[i]])

                if current_time >time_stop_input:

                    if  search_in_transaction_doc(FINAL_INSTRUMENT_ID[i],FINAL_INDEX[i],'signal')==1:

                        FINAL_POSITION[i]=-1
                        update_in_initial_doc(FINAL_INSTRUMENT_ID[i],FINAL_INDEX[i],'position',-1)
                        update_in_initial_doc(FINAL_INSTRUMENT_ID[i],FINAL_INDEX[i],'sell_price',current_price)
                        update_in_transaction_doc(FINAL_INSTRUMENT_ID[i],'sell_price',current_price)
                        update_in_transaction_doc(FINAL_INSTRUMENT_ID[i],'timestamp_sell',datetime.now())
                        update_in_transaction_doc(FINAL_INSTRUMENT_ID[i],'signal',-1)
                        SELL(EXCHANGE_ID=FINAL_INSTRUMENT_ID[i],QUANTITY=quantity[FINAL_INDEX[i]])
                                