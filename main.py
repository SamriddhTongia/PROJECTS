from main_functions import *
import pandas as pd
from datetime import datetime, time,timedelta

############check for position storing logic##################
dataframe1 = pd.read_excel('INPUT.xlsx')

values = dataframe1.values.tolist()

selection=str(values[0][0])
premium_input_nifty=(str(values[0][1]))
premium_input_Bnknifty=(str(values[0][2]))
premium_input_Finnifty=(str(values[0][3]))
time_start_input=(values[0][4])
time_stop_input=(values[0][5])
# err=str(values[0][6])
LOT_SIZE_NIFTY=values[0][6]
LOT_SIZE_BANKNIFTY=values[0][7]
LOT_SIZE_FINNIFTY=values[0][8]

symbols={1:'NIFTY',2:'BANKNIFTY',3:'FINNIFTY'}
FINAL_PREMIUM=[]
FINAL_STRIKE=[]
FINAL_INSTRUMENTS=[]
FINAL_INDEX=[]
FINAL_POSITION=[]
FINAL_INSTRUMENT_ID=[]
FINAL_EXPIRY=[]
exchange_id_list=[]
strike_prices_list=[]
initial_premium=[]
index=[]
position=[]
instruments=[]
expiry_date=[]
choices = selection.split()
i=0
COUNTNF = db['NIFTY'].count_documents({})
COUNTBNK = db['BANKNIFTY'].count_documents({})
COUNTFNF = db['FINNIFTY'].count_documents({})
if COUNTNF==10 & COUNTBNK==10 & COUNTFNF==10:
    err='no'
else:
    err='yes'

#####################    PROCESS THE CHOICES AND FILL IN THE LISTS   ######################
for choice in choices:
    current_time = datetime.now().time()
    while True and err.lower()=='yes':
        current_time = datetime.now().time()
        if (current_time >= dt.time(time_start_input.hour,time_start_input.minute-2)) and (current_time <= dt.time(time_start_input.hour,time_start_input.minute+3)) and i==0:
            socket_instruments_subscribing(symbols[1])
            socket_instruments_subscribing(symbols[2])
            socket_instruments_subscribing(symbols[3])
            i+=1
            break
    if '1' in choice:
        result = db[symbols[1]].find().sort('_id', 1)
        for document in result:
            exchange_id_list.append(document['exchange_instrument_id'])
            strike_prices_list.append(document['strike_price'])
            initial_premium.append(document['initial_premium'])
            index.append(document['symbol'])
            position.append(document['position'])
            instruments.append({'exchangeSegment':2,'exchangeInstrumentID':document['exchange_instrument_id']})
            expiry_date.append(document['expiry'])
        if (premium_input_nifty.lower()=='all'):
            FINAL_PREMIUM.extend(initial_premium)
            FINAL_EXPIRY.extend(expiry_date)
            FINAL_INDEX.extend(index)
            FINAL_POSITION.extend(position)
            FINAL_INSTRUMENT_ID.extend(exchange_id_list)
            FINAL_STRIKE.extend(strike_prices_list)
            FINAL_INSTRUMENTS.extend(instruments)
        else:
            print(initial_premium)
            lst=find_closest_positions(initial_premium,(premium_input_nifty))
            for i in lst:
                FINAL_PREMIUM.append(initial_premium[i])
                FINAL_EXPIRY.append(expiry_date[i])
                FINAL_INDEX.append(index[i])
                FINAL_POSITION.append(position[i])
                FINAL_INSTRUMENT_ID.append(exchange_id_list[i])
                FINAL_STRIKE.append(strike_prices_list[i])
                FINAL_INSTRUMENTS.append(instruments[i])

    if '2' in choice:
        exchange_id_list=[]
        strike_prices_list=[]
        initial_premium=[]
        index=[]
        position=[]
        instruments=[]
        expiry_date=[]
        result = db[symbols[2]].find().sort('_id', 1)
        for document in result:
            exchange_id_list.append(document['exchange_instrument_id'])
            strike_prices_list.append(document['strike_price'])
            initial_premium.append(document['initial_premium'])
            index.append(document['symbol'])
            position.append(document['position'])
            instruments.append({'exchangeSegment':2,'exchangeInstrumentID':document['exchange_instrument_id']})
            expiry_date.append(document['expiry'])
        if (premium_input_Bnknifty.lower()=='all'):
            FINAL_PREMIUM.extend(initial_premium)
            FINAL_EXPIRY.extend(expiry_date)
            FINAL_INDEX.extend(index)
            FINAL_POSITION.extend(position)
            FINAL_INSTRUMENT_ID.extend(exchange_id_list)
            FINAL_STRIKE.extend(strike_prices_list)
            FINAL_INSTRUMENTS.extend(instruments)
        else:
            lst=find_closest_positions(initial_premium,(premium_input_Bnknifty))
            for i in lst:
                FINAL_PREMIUM.append(initial_premium[i])
                FINAL_EXPIRY.append(expiry_date[i])
                FINAL_INDEX.append(index[i])
                FINAL_POSITION.append(position[i])
                FINAL_INSTRUMENT_ID.append(exchange_id_list[i])
                FINAL_STRIKE.append(strike_prices_list[i])
                FINAL_INSTRUMENTS.append(instruments[i])

    if '3' in choice:
        exchange_id_list=[]
        strike_prices_list=[]
        initial_premium=[]
        index=[]
        position=[]
        instruments=[]
        expiry_date=[]
        result = db[symbols[3]].find().sort('_id', 1)
        for document in result:
            exchange_id_list.append(document['exchange_instrument_id'])
            strike_prices_list.append(document['strike_price'])
            initial_premium.append(document['initial_premium'])
            index.append(document['symbol'])
            position.append(document['position'])
            instruments.append({'exchangeSegment':2,'exchangeInstrumentID':document['exchange_instrument_id']})
            expiry_date.append(document['expiry'])

        if (premium_input_Finnifty.lower()=='all'):
            FINAL_PREMIUM.extend(initial_premium)
            FINAL_EXPIRY.extend(expiry_date)
            FINAL_INDEX.extend(index)
            FINAL_POSITION.extend(position)
            FINAL_INSTRUMENT_ID.extend(exchange_id_list)
            FINAL_STRIKE.extend(strike_prices_list)
            FINAL_INSTRUMENTS.extend(instruments)
        else:
            lst=find_closest_positions(initial_premium,(premium_input_Finnifty))
            for i in lst:
                FINAL_PREMIUM.append(initial_premium[i])
                FINAL_EXPIRY.append(expiry_date[i])
                FINAL_INDEX.append(index[i])
                FINAL_POSITION.append(position[i])
                FINAL_INSTRUMENT_ID.append(exchange_id_list[i])
                FINAL_STRIKE.append(strike_prices_list[i])
                FINAL_INSTRUMENTS.append(instruments[i])