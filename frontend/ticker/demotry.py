import quandl as qd
import datetime
import math
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_validate, train_test_split,cross_val_score
from sklearn import preprocessing, svm
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer 
# Remove below and update with above
#from sklearn.preprocessing import Imputer
dt_now = datetime.datetime.today().strftime('%Y-%m-%d')
qdauth = 'JvPxndekpt7dVpVZnwLR'

def predictorModel(quote):
     
    equity='NSE/'+ quote
    #print(equity)
    
    df = qd.get(equity,start_date="2018-01-01", end_date=dt_now, authtoken = qdauth)
    df = df[['Open','Close','High','Low']]

    #Getting Features from data:
    df['HL_PCT'] = (df['High'] - df['Low']) / df['Low'] * 100.0
    df['PCT_Change'] = (df['Close'] - df['Open']) / df['Open'] * 100.0
    df = df[['Open','Close','PCT_Change','High','Low','HL_PCT']]
    
    forecast_out = int(math.ceil(0.0001*len(df)))
    #print(forecast_out)

    df['NextOpen'] = df['Open'].shift(-forecast_out)
    df['NextClose'] = df['Close'].shift(-forecast_out)
    df['NextHigh'] = df['High'].shift(-forecast_out)
    df['NextLow'] = df['Low'].shift(-forecast_out)

    #Due to Last Entity
    df.dropna(inplace=True)
    #df.tail()

    attr = ["NextOpen", "NextClose", "NextHigh", "NextLow"]
    X = np.array(df.drop(attr,1))
    X = preprocessing.scale(X)
    X_lately = X[-forecast_out:]
    df.dropna(inplace=True)

    #print(X) #will remove +e Values and Scale all the data to limit set.
    yOpen = np.array(df['NextOpen'])
    yClose = np.array(df['NextClose'])
    yHigh = np.array(df['NextHigh'])
    yLow = np.array(df['NextLow'])
    #print(len(X),len(yOpen),len(yClose),len(yHigh),len(yLow))

    X_train, X_test, yOpen_train, yOpen_test = train_test_split(X, yOpen, test_size=0.2, random_state=42)
    X_train, X_test, yClose_train, yClose_test = train_test_split(X, yClose, test_size=0.2, random_state=42)
    X_train, X_test, yHigh_train, yHigh_test = train_test_split(X, yHigh, test_size=0.2, random_state=42)
    X_train, X_test, yLow_train, yLow_test = train_test_split(X, yLow, test_size=0.2, random_state=42)

    predModel = LinearRegression(n_jobs=-1)

    #Open
    predModel.fit(X_train,yOpen_train)
    accuracyOpen = predModel.score(X_test,yOpen_test)
    print(accuracyOpen)
    forecast_setOpen = predModel.predict(X_lately)
    print(forecast_setOpen, accuracyOpen, forecast_out)

    #Close
    predModel.fit(X_train,yClose_train)
    accuracyClose = predModel.score(X_test,yClose_test)
    print(accuracyClose)
    forecast_setClose = predModel.predict(X_lately)
    print(forecast_setClose, accuracyClose, forecast_out)

    #High
    predModel.fit(X_train,yHigh_train)
    accuracyHigh = predModel.score(X_test,yHigh_test)
    print(accuracyHigh)
    forecast_setHigh = predModel.predict(X_lately)
    print(forecast_setHigh, accuracyHigh, forecast_out)

    #Low
    predModel.fit(X_train,yLow_train)
    accuracyLow = predModel.score(X_test,yLow_test)
    print(accuracyLow)
    forecast_setLow = predModel.predict(X_lately)
    print(forecast_setLow, accuracyLow, forecast_out)

    predPipeline = make_pipeline(SimpleImputer(), predModel) #----
    #Remove below and update with above for future version
    
    #predPipeline = make_pipeline(Imputer(), predModel) #----
    scoresOpen = cross_val_score(predPipeline, X, yOpen, cv=5, scoring='neg_mean_absolute_error')
    #print('Open Mean Absolute Error %2f' %(-1 * scoresOpen.mean()))

    scoresClose = cross_val_score(predPipeline, X, yClose, cv=5, scoring='neg_mean_absolute_error')
    #print('Close Mean Absolute Error %2f' %(-1 * scoresClose.mean()))

    scoresHigh = cross_val_score(predPipeline, X, yHigh, cv=5, scoring='neg_mean_absolute_error')
    #print('High Mean Absolute Error %2f' %(-1 * scoresHigh.mean()))

    scoresLow = cross_val_score(predPipeline, X, yLow, cv=5, scoring='neg_mean_absolute_error')
    #print('Low Mean Absolute Error %2f' %(-1 * scoresLow.mean()))

    finalOpen = forecast_setOpen[0] - (-1 * scoresOpen.mean())
    finalClose = forecast_setClose[0] - (-1 * scoresClose.mean())
    finalHigh = forecast_setHigh[0] - (-1 * scoresHigh.mean())
    finalLow = forecast_setLow[0] - (-1 * scoresLow.mean())

    
    context_all = {
        "Algorithm" : "Linear Regression",
        "Eq_Symbol" : quote,
        "open": { 
            "predictedOpen" : float(forecast_setOpen[0]),
            "pOpenAcc" : accuracyOpen*100,
            "OMAE": (-1 * scoresOpen.mean()),
            "finalOpen": float(finalOpen),
            },
        "close": {
            "predictedClose" : forecast_setClose[0],
            "pCloseAcc" : accuracyClose*100,
            "CMAE": (-1 * scoresClose.mean()),
            "finalClose": finalClose,
            },
        "high": {
            "predictedHigh" : forecast_setHigh[0],
            "pHighAcc" : accuracyHigh*100,
            "HMAE": (-1 * scoresHigh.mean()),
            "finalHigh": finalHigh,
            },
        "low":{
            "predictedLow" : forecast_setLow[0],
            "pLowAcc" : accuracyLow*100,
            "LMAE": (-1 * scoresLow.mean()),
            "finalLow": finalLow,
            },
        }
    return context_all

#context_v = predictorModel("WIPRO")
#print(context_v)