from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditPofileForm, ChangePasswordForm

from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader

from ticker.backend import merge_dicts, tickerIndices, getGL, getHomeNews, eqlist, equitydataAPI, equitywiki, equitydataRefresh, equitydataNews, equitydataPeer, equitydataCharts, equitydataChartsdef
from ticker.predictor import predictorModel

import requests
from nsetools import Nse
from pprint import pprint
nse = Nse()

#################################################
urlmain = 'http://127.0.0.1:8000/quoteAPI/v1/{}'#
#################################################


def home(request):
    context_all = merge_dicts(tickerIndices(), getGL(), getHomeNews())
    return render(request, 'home.html',context_all)


# About
def team(request):
    return render(request, 'about/team.html', {})

def careers(request):
    return render(request, 'about/careers.html', {})


# Pricing
def pricing(request):
    return render(request, 'pricing.html', {})


# Services
def services(request):
    return render(request, 'services.html', {})


# API

def quoteAPI(request,symbol):
    if nse.is_valid_code(symbol):
        context_all = equitydataAPI(symbol)
        return JsonResponse(context_all, safe=False)
    else:
        return handler404(request)

  


# Pages
def equitylist(request):
    data = eqlist()
    return render(request, 'equitylist.html', context= {'data':data})


# Equity

def autoRefreshEqu(request,symbol):
    if nse.is_valid_code(symbol):
        context_all = equitydataRefresh(symbol)
        return render(request,'equity/autorefequ.html',context_all )


def equity(request,symbol):
    import pandas as pd
    from datetime import datetime, date, time
    from nsepy import get_history
        
        
    if nse.is_valid_code(symbol):
        x = equitydataAPI(symbol)
        x = x['data'][0]

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date and end_date:
            context = equitydataCharts(symbol,start_date,end_date)
        else:
            context = equitydataChartsdef(symbol)
        
        context_all = {
            'symbol': symbol,
            'compDet': equitywiki(symbol),
            'quoteNews' : equitydataNews(symbol),
            'peerlist': equitydataPeer(symbol),
            'x': x,          
            'quote':quote,
            #'changeQuote':changeQuote,
            }

        context_all = merge_dicts(context, context_all)
        
        
        template = loader.get_template('equity/equity.html')
        response_body = template.render(context_all,request)
        return HttpResponse(response_body)


'''
def quote(request):
    # Getting Value From HTML Input
    if request.method == "POST":
        #quote = request.POST["quote"]
        quote = request.POST.get('quote', '').strip().split(' ')[0].strip().upper()
        print("Requested Quote : ",quote)
        # Getting Value's From NSE API 
        x = nse.get_quote(quote)
        print(x)
        changeQuote = float(x['change'])     
        cName = (x['companyName'])
        print(cName)
        cURL = "https://newsapi.org/v2/everything?q="+ cName +"&apiKey=2c9f31acb8cc466bbf2647cf4170b81d"
        #print(cURL)
        quoteNewsSet = (requests.get(cURL)).json
        context_all = {'quote':quote,'x':x,'changeQuote':changeQuote, 'cName':cName, 'quoteNews':quoteNewsSet }
        return render(request, 'quote.html', context_all)
    else:
        return handler404(request)

'''
def quote(request):
    # Getting Value From HTML Input
    if request.method == "POST":
        quote = request.POST["quote"]
        if nse.is_valid_code(quote):
            return quote_data(request,quote)
        else:
            return handler404(request)
    else:
        return handler404(request)

  


def quote_data(request, symbol):
    x = nse.get_quote(symbol)
    changeQuote = float(x['change'])
    cName = (x['companyName'])
    demoname = cName.split()[:int(len(cName)/2)]
    #demoname = demoname
    demoname = ' '.join(demoname)
    descCompany = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={}".format(demoname)
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
    
    import json
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

    print(peerlist)
    
    
    
    
    cURL = "https://newsapi.org/v2/everything?q="+ cName +"&apiKey=2c9f31acb8cc466bbf2647cf4170b81d"
    quoteNewsSet = (requests.get(cURL)).json

    import quandl as qd
    import pandas as pd
    import datetime
    dtnow = datetime.datetime.today().strftime("%d-%b-%Y")
    dt_now = datetime.datetime.today().strftime("%d-%b-%Y %H:%M:%S")
    qdauth = 'JvPxndekpt7dVpVZnwLR'
    equity = 'NSE/' + symbol
    #####
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:    
        df = qd.get(equity,start_date=start_date, end_date=end_date, authtoken = qdauth)
    else:
        df = qd.get(equity,start_date="2018-01-01", end_date=dtnow, authtoken = qdauth)
    
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d').dt.strftime("%Y-%m-%d")
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

    context_all = {'quote':quote, 'peerlist':peerlist  ,'x':x,'changeQuote':changeQuote, 'cName':cName, 'quoteNews':quoteNewsSet, 'contextOpen' : contextOpen,
        'contextClose' : contextClose,
        'contextHigh' : contextHigh,
        'contextLow' : contextLow,
        'contextOC': contextOC,
        'contextHL' : contextHL,
        'dt_now':dt_now,
        'compDet':compDet }
    template = loader.get_template('quote-data.html')
    response_body = template.render(context_all,request)
    return HttpResponse(response_body)

    
#'''
#except ConnectionAbortedError:
#    return HttpResponse(''' ConnectionAbortedError ''')

#except :
#    return render(request, 'server-error.html', {'symbol':symbol})
#'''

def api_req(request, symbol):
    context_all = predictorModel(symbol)
    #context_all = {"symbol":symbol}
    return JsonResponse(context_all)

def chartstd(request):
    import quandl as qd
    import pandas as pd
    import datetime
    dt_now = datetime.datetime.today().strftime('%Y-%m-%d')
    qdauth = 'JvPxndekpt7dVpVZnwLR'
    
    #####
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:    
        df = qd.get('NSE/BAJFINANCE',start_date=start_date, end_date=end_date, authtoken = qdauth)
    else:
        df = qd.get('NSE/BAJFINANCE',start_date="2018-01-01", end_date=dt_now, authtoken = qdauth)
    
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d').dt.strftime("%Y-%m-%d")
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

    context_all = {
        'contextOpen' : contextOpen,
        'contextClose' : contextClose,
        'contextHigh' : contextHigh,
        'contextLow' : contextLow,
        'contextOC': contextOC,
        'contextHL' : contextHL,
    }
    #return HttpResponse(context_all)
    return render(request, 'chartstd/chartstd.html', context_all)



# Authentication

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("Successful Login!"))
            return redirect('home')
        else:
            messages.success(request,("Error Login in!"))            
            return redirect('login')
    else:
        return render(request, "authenticate/login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request,("Successful Logout!"))
    return redirect('home')

def signup_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request,("Successful Reg.!"))
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, "authenticate/signup.html", {'form':form})

def edit_profile(request):
    if request.method == "POST":
        form = EditPofileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,("Successful Change"))
            return redirect('home')
    else:
        form = EditPofileForm(instance=request.user)

    return render(request, "authenticate/edit_profile.html", {'form':form})

def password_change(request):
    if request.method == "POST":
        form = ChangePasswordForm(data = request.POST, user =request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,("Password Successful Change"))
            return redirect('home')
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request,"authenticate/password_change.html",{'form':form})

# Error Handlers

def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)