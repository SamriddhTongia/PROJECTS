from Connect import XTSConnect
# Interactive API Credentials
API_KEY = "2ac2721d705f5ebf008683"
API_SECRET = "Auyh328##5"
clientID = "BP999"
userID = "YOUR_USER_ID_HERE"
XTS_API_BASE_URL = "https://xts.indiratrade.com/"
source = "WEBAPI"


"Note : For dealer credentials add the clientID and for investor client leave the clientID blank"

"""Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
xt = XTSConnect(API_KEY, API_SECRET, source)

"""Using the xt object we created call the interactive login Request"""
response = xt.interactive_login()
print("Login: ", response)
"""Order book Request"""
clientID = "BP999"

def BUY(EXCHANGE_ID,QUANTITY):
    # response = xt.place_order(
    #     exchangeSegment=xt.EXCHANGE_NSEFO,
    #     exchangeInstrumentID=EXCHANGE_ID,
    #     productType=xt.PRODUCT_NRML,
    #     orderType=xt.ORDER_TYPE_MARKET,
    #     orderSide=xt.TRANSACTION_TYPE_BUY,
    #     timeInForce=xt.VALIDITY_DAY,
    #     disclosedQuantity=0,
    #     orderQuantity=QUANTITY,
    #     limitPrice=0,
    #     stopPrice=0,
    #     orderUniqueIdentifier="454845",
    #     clientID=clientID)
    print("Place Order: ", response)

def SELL(EXCHANGE_ID,QUANTITY):
    # response = xt.place_order(
    #     exchangeSegment=xt.EXCHANGE_NSEFO,
    #     exchangeInstrumentID=EXCHANGE_ID,
    #     productType=xt.PRODUCT_NRML,
    #     orderType=xt.ORDER_TYPE_MARKET,
    #     orderSide=xt.TRANSACTION_TYPE_SELL,
    #     timeInForce=xt.VALIDITY_DAY,
    #     disclosedQuantity=0,
    #     orderQuantity=QUANTITY,
    #     limitPrice=0,
    #     stopPrice=0,
    #     orderUniqueIdentifier="454845",
    #     clientID=clientID)
    print("Place Order: ", response)

