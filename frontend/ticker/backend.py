import random
import json
import requests
from bs4 import BeautifulSoup

import pandas as pd
from datetime import datetime, date, time
from nsepy import get_history


from nsetools import Nse
nse = Nse()


#################################################
urlmain = 'http://127.0.0.1:8000/quoteAPI/v1/{}'#
#################################################


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

    ssymbol0 = symbol0["indices"]["direction"]
    ssymbol1 = symbol1["indices"]["direction"]
    ssymbol2 = symbol2["indices"]["direction"]
    ssymbol3 = symbol3["indices"]["direction"] 
    ssymbol4 = symbol4["indices"]["direction"]
    ssymbol5 = symbol5["indices"]["direction"]
    ssymbol6 = symbol6["indices"]["direction"]
    ssymbol7 = symbol7["indices"]["direction"]
    ssymbol8 = symbol8["indices"]["direction"]
    ssymbol9 = symbol9["indices"]["direction"]
    ssymbol10 = symbol10["indices"]["direction"]
    ssymbol11 = symbol11["indices"]["direction"]
    ssymbol12 = symbol12["indices"]["direction"]
    ssymbol13 = symbol13["indices"]["direction"]
    ssymbol14 = symbol14["indices"]["direction"]

    contextall = {
        "symbol0":symbol0,
        "symbol1":symbol1,
        "symbol2":symbol2,
        "symbol3":symbol3,
        "symbol4":symbol4,
        "symbol5":symbol5,
        "symbol6":symbol6,
        "symbol7":symbol7,
        "symbol8":symbol8,
        "symbol9":symbol9,
        "symbol10":symbol10,
        "symbol11":symbol11,
        "symbol12":symbol12,
        "symbol13":symbol13,
        "symbol14":symbol14,
        "ssymbol0":int(ssymbol0),
        "ssymbol1":int(ssymbol1),
        "ssymbol2":int(ssymbol2),
        "ssymbol3":int(ssymbol3),
        "ssymbol4":int(ssymbol4),
        "ssymbol5":int(ssymbol5),
        "ssymbol6":int(ssymbol6),
        "ssymbol7":int(ssymbol7),
        "ssymbol8":int(ssymbol8),
        "ssymbol9":int(ssymbol9),
        "ssymbol10":int(ssymbol10),
        "ssymbol11":int(ssymbol11),
        "ssymbol12":int(ssymbol12),
        "ssymbol13":int(ssymbol13),
        "ssymbol14":int(ssymbol14),
        }
    return contextall



def getGL():
    gain = nse.get_top_gainers()

    loss = nse.get_top_losers()
    
    USD_INR = (requests.get("https://priceapi.moneycontrol.com/pricefeed/notapplicable/currencyspot/%24%24%3BUSDINR")).json()
    EUR_INR = (requests.get("https://priceapi.moneycontrol.com/pricefeed/notapplicable/currencyspot/%24%24%3BEURINR")).json()
    GBP_INR = (requests.get("https://priceapi.moneycontrol.com/pricefeed/notapplicable/currencyspot/%24%24%3BGBPINR")).json()

    contextall = {
        "gain":gain,
        "loss":loss,
        "USD_INR":USD_INR,
        "EUR_INR":EUR_INR,
        "GBP_INR":GBP_INR
        }
    return contextall



def getHomeNews():
    
    autoscrollnews_set = (requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=2c9f31acb8cc466bbf2647cf4170b81d")).json
    homeNewsSet = (requests.get("https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=2c9f31acb8cc466bbf2647cf4170b81d")).json
    newsroller = (requests.get("https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=2c9f31acb8cc466bbf2647cf4170b81d")).json
    
    contextall = {
        "autoscrollnews_set":autoscrollnews_set,
        "homeNews":homeNewsSet,
        "newsroller":newsroller
        }
    return contextall



def eqlist():
    with open("ticker/EQList.json") as f:
        data = json.load(f)
    return data



def equitydataAPI(symbol):
    url = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={}".format(symbol)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    data = soup.find_all(id="responseDiv")
    data = str(data)
    data = data.replace('[<div id="responseDiv" style="display:none">\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n{', "{")
    data = data.replace("}\r\n\r\n\r\n</div>]", "}")
    data = json.loads(data)


    url2 = "https://www.google.co.in/search?q={}".format(symbol)
    req= requests.get(url2)
    soup2 = BeautifulSoup(req.text, 'html.parser')
    
    context_all = {
        "tradedDate" : data["tradedDate"],
        "lastUpdateTime": data["lastUpdateTime"],
        "data" : [
            {
                "pricebandupper" : data["data"][0]["pricebandupper"],
                "symbol" : data["data"][0]["symbol"],
                "wikiname" : soup2.find("div", {"class": "FSP1Dd"}).text,
                "companytype" : soup2.find("div", {"class": "F7uZG Rlw09"}).text,
                "applicableMargin" :data["data"][0]["applicableMargin"],
                "bcEndDate": data["data"][0]["bcEndDate"],
                "totalSellQuantity": data["data"][0]["totalSellQuantity"],
                "adhocMargin": data["data"][0]["adhocMargin"],
                "companyName": data["data"][0]["companyName"],
                "marketType": data["data"][0]["marketType"],
                "exDate": data["data"][0]["exDate"],
                "bcStartDate": data["data"][0]["bcStartDate"],
                "css_status_desc": data["data"][0]["css_status_desc"],
                "dayHigh": data["data"][0]["dayHigh"],
                "basePrice": data["data"][0]["basePrice"],
                "securityVar": data["data"][0]["securityVar"],
                "pricebandlower": data["data"][0]["pricebandlower"],
                "sellQuantity5": data["data"][0]["sellQuantity5"],
                "sellQuantity4": data["data"][0]["sellQuantity4"],
                "sellQuantity3": data["data"][0]["sellQuantity3"],
                "sellQuantity2": data["data"][0]["sellQuantity2"],
                "sellQuantity1":data["data"][0]["sellQuantity1"],
                "cm_adj_high_dt": data["data"][0]["cm_adj_high_dt"],
                "dayLow": data["data"][0]["dayLow"],
                "quantityTraded": data["data"][0]["quantityTraded"],
                "pChange": data["data"][0]["pChange"],
                "totalTradedValue": data["data"][0]["totalTradedValue"],
                "deliveryToTradedQuantity": data["data"][0]["deliveryToTradedQuantity"],
                "totalBuyQuantity": data["data"][0]["totalBuyQuantity"],
                "averagePrice": data["data"][0]["averagePrice"],
                "indexVar": data["data"][0]["indexVar"],
                "cm_ffm": data["data"][0]["cm_ffm"],
                "purpose": data["data"][0]["purpose"],
                "buyPrice2": data["data"][0]["buyPrice2"],
                "secDate": data["data"][0]["secDate"],
                "buyPrice1": data["data"][0]["buyPrice1"],
                "high52": data["data"][0]["high52"],
                "previousClose": data["data"][0]["previousClose"],
                "ndEndDate": data["data"][0]["ndEndDate"],
                "low52": data["data"][0]["low52"],
                "buyPrice4": data["data"][0]["buyPrice4"],
                "buyPrice3": data["data"][0]["buyPrice3"],
                "recordDate": data["data"][0]["recordDate"],
                "deliveryQuantity": data["data"][0]["deliveryQuantity"],
                "buyPrice5": data["data"][0]["buyPrice5"],
                "priceBand": data["data"][0]["priceBand"],
                "extremeLossMargin": data["data"][0]["extremeLossMargin"],
                "cm_adj_low_dt": data["data"][0]["cm_adj_low_dt"],
                "varMargin": data["data"][0]["varMargin"],
                "sellPrice1": data["data"][0]["sellPrice1"],
                "sellPrice2": data["data"][0]["sellPrice2"],
                "totalTradedVolume": data["data"][0]["totalTradedVolume"],
                "sellPrice3": data["data"][0]["sellPrice3"],
                "sellPrice4": data["data"][0]["sellPrice4"],
                "sellPrice5": data["data"][0]["sellPrice5"],
                "change": data["data"][0]["change"],
                "surv_indicator": data["data"][0]["surv_indicator"],
                "ndStartDate": data["data"][0]["ndStartDate"],
                "buyQuantity4": data["data"][0]["buyQuantity4"],
                "isExDateFlag": data["data"][0]["isExDateFlag"],
                "buyQuantity3": data["data"][0]["buyQuantity3"],
                "buyQuantity2": data["data"][0]["buyQuantity2"],
                "buyQuantity1": data["data"][0]["buyQuantity1"],
                "series": data["data"][0]["series"],
                "faceValue": data["data"][0]["faceValue"],
                "buyQuantity5": data["data"][0]["buyQuantity5"],
                "closePrice": data["data"][0]["closePrice"],
                "open": data["data"][0]["open"],
                "isinCode": data["data"][0]["isinCode"],
                "lastPrice": data["data"][0]["lastPrice"]
                }]}

    return context_all



def equitywiki(symbol):
    x = requests.get(urlmain.format(symbol)).json()
    cname = (x['data'][0]['wikiname'])
    descCompany = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={}".format(cname)
    wsSet = (requests.get(descCompany)).json()
    param = list(wsSet['query']['pages'].keys())
    param = "".join(param)
    title = wsSet['query']['pages'][param]['title']
    extract = wsSet['query']['pages'][param]['extract']
    url2 = ("https://en.wikipedia.org/api/rest_v1/page/summary/{}".format(title))
    nSet = (requests.get(url2)).text
    nsSet = (requests.get(url2)).json()
    if 'thumbnail' in nSet:
        imgurl = (nsSet['thumbnail']['source'])
    else:
        imgurl = "data:image/gif;base64,R0lGODlhAQABAIAAAHd3dwAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw=="

    url2 = (nsSet['content_urls']['desktop']['page'])
    compDet = {
        'title' : title,
        'extract' : extract,
        'url2':url2,
        'imgurl':imgurl
    }
    return compDet



def equitydataRefresh(symbol):           
    x = requests.get(urlmain.format(symbol)).json()

    context_all = {
    'changeQuote': float(x['data'][0]['change']),
    'lastPrice': x['data'][0]['lastPrice'],
    'change':x['data'][0]['change'],
    'pChange':x['data'][0]['pChange'],
    'lastUpdateTime': x['lastUpdateTime'],
    }
    return context_all



def equitydataNews(symbol):
    x = requests.get(urlmain.format(symbol)).json()
    cname = (x['data'][0]['wikiname'])
    cURL = "https://newsapi.org/v2/everything?q="+ cname +"&apiKey=2c9f31acb8cc466bbf2647cf4170b81d"
    quoteNewsSet = (requests.get(cURL)).json
    return quoteNewsSet



def equitydataPeer(symbol):
    peerurl = ("https://nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxPeerCompanies.jsp?symbol={}").format(symbol)
    r  = requests.get(peerurl)
    data = r.text
    data = data.replace('\r', '')
    data = data.replace('\n', '')
    data = data.replace('industry', '"industry"', 1)
    data = data.replace('data', '"data"', 1)
    jdata = json.loads(data)
    r = json.dumps(jdata)
    loaded_r = json.loads(r)
    keys = []
    values = []
    
    for key in range(0,len(loaded_r['data'])):
        symbol_c = loaded_r['data'][key]["symbol"]
        keys.append(symbol_c)
    
    for value in range(0,len(loaded_r['data'])):
        symbol_c = loaded_r['data'][value]["name"]
        values.append(symbol_c)

    peerlist = dict(zip(keys, values))
    return peerlist




def equitydataCharts(symbol,start_date,end_date):
    import pandas as pd
    from datetime import datetime, date, time
    from nsepy import get_history

    eq = symbol
    start_date = start_date
    end_date = end_date

    startdt = datetime.strptime(start_date, "%Y-%m-%d").date()
    enddt = datetime.strptime(end_date, "%Y-%m-%d").date()
    df = get_history(symbol = eq, start=startdt, end=enddt) 

    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    dfOpen = df[['Date','Open']]
    dfClose = df[['Date','Close']]
    dfHigh = df[['Date','High']]
    dfLow = df[['Date','Low']]
    dfOC = df[['Date','Open', 'Close']]
    dfHL = df[['Date','High', 'Low']]

    contextOpen = dfOpen.to_json(orient='records')
    contextClose = dfClose.to_json(orient='records')
    contextHigh = dfHigh.to_json(orient='records')
    contextLow = dfLow.to_json(orient='records')
    contextOC = dfOC.to_json(orient='records')
    contextHL = dfHL.to_json(orient='records')

    context_all = {'contextOpen' : contextOpen,
    'contextClose' : contextClose,
    'contextHigh' : contextHigh,
    'contextLow' : contextLow,
    'contextOC': contextOC,
    'contextHL' : contextHL}

    return context_all


def equitydataChartsdef(symbol):

    eq = symbol
    startdt = datetime.strptime("2019-01-01", "%Y-%m-%d").date()
    enddt= date.today()
    df = get_history(symbol = eq, start=startdt, end=enddt)

    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    dfOpen = df[['Date','Open']]
    dfClose = df[['Date','Close']]
    dfHigh = df[['Date','High']]
    dfLow = df[['Date','Low']]
    dfOC = df[['Date','Open', 'Close']]
    dfHL = df[['Date','High', 'Low']]

    contextOpen = dfOpen.to_json(orient='records')
    contextClose = dfClose.to_json(orient='records')
    contextHigh = dfHigh.to_json(orient='records')
    contextLow = dfLow.to_json(orient='records')
    contextOC = dfOC.to_json(orient='records')
    contextHL = dfHL.to_json(orient='records')

    context_all = {'contextOpen' : contextOpen,
    'contextClose' : contextClose,
    'contextHigh' : contextHigh,
    'contextLow' : contextLow,
    'contextOC': contextOC,
    'contextHL' : contextHL}

    return context_all
