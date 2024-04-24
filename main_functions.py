from Connect import XTSConnect
from datetime import datetime
import json
from datetime import datetime, time
from time import sleep
from pymongo import MongoClient
import datetime as dt
import pymongo

##########   MONGODB CONNECTION  ###############
client = MongoClient('mongodb://localhost:27017/')
db = client['backend12']
collection = db['transaction_sheet']
collection1=db['entry']
##################################################


#################### Marketdata API Credentials ##################
API_KEY = "88a85e1ab0e12049bdf453"
API_SECRET = "Dsti357$at"
XTS_API_BASE_URL = "https://xts-api.trading"
source = "WEBAPI"
###################################################################

####################LOGIN################################
"""Make the XTSConnect Object with Marketdata API appKey, secretKey and source"""
xt = XTSConnect(API_KEY, API_SECRET, source)

"""Using the object we call the login function Request"""
response = xt.marketdata_login()
###########################################################

#####################################FUNCTIONS#######################################

def get_expiry_date_future(SYMBOL):
    """GET THE EXPIRY OF THE FUTURE"""
    response = xt.get_expiry_date(
    exchangeSegment=2,
    series='FUTIDX',
    symbol=SYMBOL)
    exp_date=response['result']
    exp_date.sort()
    target_date= datetime.strptime(exp_date[0], "%Y-%m-%dT%H:%M:%S").date()
    # Convert to datetime object
    target_date = datetime.strptime(str(target_date), "%Y-%m-%d")
    # Convert to the desired format
    target_date = target_date.strftime("%d%b%Y")
    return target_date

def get_expiry_date_option(SYMBOL):
    """GET THE EXPIRY OF THE OPTION"""
    response = xt.get_expiry_date(
    exchangeSegment=2,
    series='OPTIDX',
    symbol=SYMBOL)
    exp_date=response['result']
    exp_date.sort()
    target_date= datetime.strptime(exp_date[0], "%Y-%m-%dT%H:%M:%S").date()
    # Convert to datetime object
    target_date = datetime.strptime(str(target_date), "%Y-%m-%d")
    # Convert to the desired format
    target_date = target_date.strftime("%d%b%Y")
    return target_date




def get_strike_price(SYMBOL):
    """Get Strike Prices(4 OTM HERE)"""
    response = xt.get_future_symbol(
        exchangeSegment=2,
        series='FUTIDX',
        symbol=SYMBOL,
        expiryDate=get_expiry_date_future(SYMBOL)
        )
    exchange_instrument_id=response['result'][0]['ExchangeInstrumentID']
    instruments=[{'exchangeSegment': 2, 'exchangeInstrumentID': exchange_instrument_id}]
    """Get Quote Request"""
    response = xt.get_quote(
        Instruments=instruments,
        xtsMessageCode=1512,
        publishFormat='JSON')
    #taking out the last traded price
    li=response['result']['listQuotes'][0]
    last_traded_price = json.loads(li)['LastTradedPrice']
    #calculate the strike price
    all_strikes=[]
    strike_price=int(last_traded_price/100)*100
    for offset in range(-400, 500, 100):
        if offset!=0:
            all_strikes.append(strike_price + offset)
        else:
                all_strikes.append(strike_price + offset)
                all_strikes.append(strike_price + offset)

    return all_strikes

def socket_instruments_subscribing(SYMBOL):
    """GETTING THE EXCHANGE INSTRUMENT ID FOR SUBSCRIBING
    RETURNS STRIKE_PRICE LIST,EXCHANGE_INSTRUMENT_ID LIST AND INSTRUMENTS FOR SUBSCRIPTION"""
    collection2=db[SYMBOL]
    expiry=get_expiry_date_option(SYMBOL)
    strikes=get_strike_price(SYMBOL)
    half=int(len(strikes)/2)
    for element in strikes[:half]:
        current_time = datetime.now().time()
        """Get Option Symbol Request"""
        response = xt.get_option_symbol(
        exchangeSegment=2,
        series='OPTIDX',
        symbol=SYMBOL,
        expiryDate=expiry,
        optionType='PE',
        strikePrice=element)

        SCRIP=response['result'][0]['ExchangeInstrumentID']
        instrument_quote=[{'exchangeSegment': 2, 'exchangeInstrumentID': SCRIP}]


        """Get Quote Request"""
        response = xt.get_quote(
        Instruments=instrument_quote,
        xtsMessageCode=1512,
        publishFormat='JSON')

        li=response['result']['listQuotes'][0]
        initial_value={
                'strike_price':element,
                'exchange_instrument_id':SCRIP,
                'initial_premium':json.loads(li)['LastTradedPrice'],
                'buy_price':0,
                'sell_Price':0,
                'expiry':expiry,
                'position':0,
                'option_type':'PE',
                'symbol':SYMBOL
            }
        collection2.insert_one(initial_value)
        
    for element in strikes[half:]:
        current_time = datetime.now().time()
        """Get Option Symbol Request"""
        response = xt.get_option_symbol(
        exchangeSegment=2,
        series='OPTIDX',
        symbol=SYMBOL,
        expiryDate=expiry,
        optionType='CE',
        strikePrice=element)
        SCRIP=response['result'][0]['ExchangeInstrumentID']
        instrument_quote=[{'exchangeSegment': 2, 'exchangeInstrumentID': SCRIP}]


        """Get Quote Request"""
        response = xt.get_quote(
        Instruments=instrument_quote,
        xtsMessageCode=1512,
        publishFormat='JSON')

        li=response['result']['listQuotes'][0]
        initial_value={
                'strike_price':element,
                'exchange_instrument_id':SCRIP,
                'initial_premium':json.loads(li)['LastTradedPrice'],
                'buy_price':0,
                'sell_price':0,
                'expiry':expiry,
                'position':0,
                'option_type':'CE',
                'symbol':SYMBOL
            }
        
        collection2.insert_one(initial_value)

    return 0

def update_in_initial_doc(Id,SYMBOL,field,value):
    """FIRST PUT EXCHANGE_INSTRUMENT_ID THEN THE CORRESPONDING INDEX NAME THEN WHAT FIELD YOU WANT(as string) TO CHANGE AND THEN THE FIELDS VALUE"""
    query = {'exchange_instrument_id': Id}
    db[SYMBOL].update_one(query, {'$set': {field: value}})


    
def update_in_transaction_doc(Id,field,value):
    query = {'exchange_id': Id}
    update = {'$set': {field: value}}
    collection.update_one(query, update)

def store_signal(index,initial_price,signal_value,buy_price,strike_prc,type,id,expiry,quantity):
    signal_data = {
        'index':index,
        'initial_price':initial_price,
        'signal':signal_value,
        'timestamp_buy': datetime.now(),
        'timestamp_sell':'',
        'buy_price':buy_price,
        'sell_price':0,
        'type':type,
        'expiryDate':expiry,
        'strike_price':strike_prc,
        'exchange_id':id,
        'quantity':quantity
    }
    collection.insert_one(signal_data)

def search_in_initial_doc(Id,Symbol,Field):
    """SEARCH IN THE INITIAL DOC OF THE PARTICULAR SYMBOL FOR DESIRED FIELD PUT EXCHANGE_ID,INDEX_NAME AND FIELD"""
    query = {'exchange_instrument_id': Id}
    results = db[Symbol].find(query)
    return results[0][Field]

def search_in_transaction_doc(Id,Symbol,Field):
    """SEARCH THE TRANSACTION DOC FOR DESIRED FIELD PUT EXCHANGE_ID AND FIELD"""
    query = {'exchange_id': Id}
    document_count = collection.count_documents(query)
    if document_count > 0:
        last_document = collection.find(query).sort('_id', pymongo.DESCENDING).limit(1)
        return last_document[0][Field]
    else:
        return 0 

def find_closest_positions(original_list,given_list):
    given_list= [int(value) for value in given_list.split(',')]
    closest_indices = []
    for num1 in given_list:
        closest_indices_for_num1 = []
        min_difference = float('inf')
        
        for index, num2 in enumerate(original_list):
            difference = abs(float(num1) - float(num2))
            if difference < min_difference:
                min_difference = difference
                closest_indices_for_num1 = [index]
            elif difference == min_difference:
                closest_indices_for_num1.append(index)

        closest_indices.extend(closest_indices_for_num1)
    return closest_indices


def calculate_stop_loss(initial_premium):
    if initial_premium >= 10 - 5 and initial_premium <= 10 + 5:
        return .50
    elif initial_premium >= 20 - 5 and initial_premium <= 20 + 5:
        return .70
    elif initial_premium >= 30 - 5 and initial_premium <= 30 + 5:
        return .75
    elif initial_premium >= 40 - 5 and initial_premium <= 40 + 5:
        return .80
    elif initial_premium >= 50 - 5 and initial_premium <= 95:
        return .85
    elif initial_premium >= 100 - 5:
        return .9
    else:
        return 0

