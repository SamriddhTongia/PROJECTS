from Connect import XTSConnect

API_KEY = "2ac2721d705f5ebf008683"
API_SECRET = "Auyh328##5"
clientID = "BP999"
userID = "DMA005"
XTS_API_BASE_URL = "https://xts.indiratrade.com/"
source = "WEBAPI"

"""Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
xt = XTSConnect(API_KEY, API_SECRET, source)

"""Using the xt object we created call the interactive login Request"""
response = xt.interactive_login()
print("Login: ", response)
"""Order book Request"""
clientID = "BP999"

