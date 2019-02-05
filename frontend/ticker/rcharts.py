import pandas as pd
from datetime import datetime, date, time
from nsepy import get_history


startdt = datetime.strptime("2018-01-01", "%Y-%m-%d").date()
enddt= date.today()
df = get_history(symbol = symbol, start=startdt, end=enddt)
print(type(df))
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

context_all = {'contextOpen' : contextOpen,
    'contextClose' : contextClose,
    'contextHigh' : contextHigh,
    'contextLow' : contextLow,
    'contextOC': contextOC,
    'contextHL' : contextHL,
    'dt_now':dt_now,
    'compDet':compDet }
















import pandas as pd
        from datetime import datetime, date, time, timedelta
        from nsepy import get_history

        if start_date and end_date:
            startdt = datetime.strptime(start_date, "%Y-%m-%d").date()
            enddt = datetime.strptime(end_date, "%Y-%m-%d").date()
            df = get_history(symbol = symbol, start=startdt, end=enddt)

        else:
            startdt = datetime.strptime("2018-01-01", "%Y-%m-%d").date()
            #enddt = date.today() - timedelta(days = 1)
            enddt= date.today()
            df = get_history(symbol = symbol, start=startdt, end=enddt)

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

                