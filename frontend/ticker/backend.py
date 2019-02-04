import random
import json
import requests

from nsetools import Nse
nse = Nse()

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def tickerIndices():
    url_set = []

    for x in range(15):
        url_set.append("http://appfeeds.moneycontrol.com/jsonapi/market/indices&ind_id={}".format(random.randint(1,81)))
    
    symbol0 = (requests.get(url_set[0])).json()
    symbol1 = (requests.get(url_set[1])).json()
    symbol2 = (requests.get(url_set[2])).json()
    symbol3 = (requests.get(url_set[3])).json()
    symbol4 = (requests.get(url_set[4])).json()
    symbol5 = (requests.get(url_set[5])).json()
    symbol6 = (requests.get(url_set[6])).json()
    symbol7 = (requests.get(url_set[7])).json()
    symbol8 = (requests.get(url_set[8])).json()
    symbol9 = (requests.get(url_set[9])).json()
    symbol10 = (requests.get(url_set[10])).json()
    symbol11 = (requests.get(url_set[11])).json()
    symbol12 = (requests.get(url_set[12])).json()
    symbol13 = (requests.get(url_set[13])).json()
    symbol14 = (requests.get(url_set[14])).json()

    ssymbol0 = symbol0['indices']['direction']
    ssymbol1 = symbol1['indices']['direction']
    ssymbol2 = symbol2['indices']['direction']
    ssymbol3 = symbol3['indices']['direction'] 
    ssymbol4 = symbol4['indices']['direction']
    ssymbol5 = symbol5['indices']['direction']
    ssymbol6 = symbol6['indices']['direction']
    ssymbol7 = symbol7['indices']['direction']
    ssymbol8 = symbol8['indices']['direction']
    ssymbol9 = symbol9['indices']['direction']
    ssymbol10 = symbol10['indices']['direction']
    ssymbol11 = symbol11['indices']['direction']
    ssymbol12 = symbol12['indices']['direction']
    ssymbol13 = symbol13['indices']['direction']
    ssymbol14 = symbol14['indices']['direction']

    contextall = {
        'symbol0':symbol0,
        'symbol1':symbol1,
        'symbol2':symbol2,
        'symbol3':symbol3,
        'symbol4':symbol4,
        'symbol5':symbol5,
        'symbol6':symbol6,
        'symbol7':symbol7,
        'symbol8':symbol8,
        'symbol9':symbol9,
        'symbol10':symbol10,
        'symbol11':symbol11,
        'symbol12':symbol12,
        'symbol13':symbol13,
        'symbol14':symbol14,
        'ssymbol0':int(ssymbol0),
        'ssymbol1':int(ssymbol1),
        'ssymbol2':int(ssymbol2),
        'ssymbol3':int(ssymbol3),
        'ssymbol4':int(ssymbol4),
        'ssymbol5':int(ssymbol5),
        'ssymbol6':int(ssymbol6),
        'ssymbol7':int(ssymbol7),
        'ssymbol8':int(ssymbol8),
        'ssymbol9':int(ssymbol9),
        'ssymbol10':int(ssymbol10),
        'ssymbol11':int(ssymbol11),
        'ssymbol12':int(ssymbol12),
        'ssymbol13':int(ssymbol13),
        'ssymbol14':int(ssymbol14),
        }
    return contextall

def getGL():
    gain = nse.get_top_gainers()

    loss = nse.get_top_losers()
    
    USD_INR = (requests.get("https://priceapi.moneycontrol.com/pricefeed/notapplicable/currencyspot/%24%24%3BUSDINR")).json()
    EUR_INR = (requests.get("https://priceapi.moneycontrol.com/pricefeed/notapplicable/currencyspot/%24%24%3BEURINR")).json()
    GBP_INR = (requests.get("https://priceapi.moneycontrol.com/pricefeed/notapplicable/currencyspot/%24%24%3BGBPINR")).json()

    contextall = {
        'gain':gain,
        'loss':loss,
        'USD_INR':USD_INR,
        'EUR_INR':EUR_INR,
        'GBP_INR':GBP_INR
        }
    return contextall

def getHomeNews():
    
    autoscrollnews_set = (requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=2c9f31acb8cc466bbf2647cf4170b81d")).json
    homeNewsSet = (requests.get("https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=2c9f31acb8cc466bbf2647cf4170b81d")).json
    newsroller = (requests.get("https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=2c9f31acb8cc466bbf2647cf4170b81d")).json
    
    contextall = {
        'autoscrollnews_set':autoscrollnews_set,
        'homeNews':homeNewsSet,
        'newsroller':newsroller
        }
    return contextall

def eqlist():
    import json

    with open('ticker/EQList.json') as f:
        data = json.load(f)
    
    return data
