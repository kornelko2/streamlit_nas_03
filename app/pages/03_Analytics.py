import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

api_key = st.secrets["ALPHA_VABTAGE_API_KEY_demo"]

st.header('Analytics')
tickers = st.text_input('Enter a ticker', 'MSFT,IBM,AAPL')
range_start = st.date_input('Start date', datetime(2023, 7, 1))
range_end = st.date_input('End date', datetime(2023, 8, 31))
url_analytics = f'https://alphavantageapi.co/timeseries/analytics?SYMBOLS={tickers}&RANGE={range_start}&RANGE={range_end}&INTERVAL=DAILY&OHLC=close&CALCULATIONS=MEAN,STDDEV,CORRELATION&apikey={api_key}'
# url_sentiment = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}'
response_analytics = requests.get(url_analytics)

st.write(url_analytics)
st.write(response_analytics.json())
if response_analytics.status_code != 200:
    st.write('Error fetching data')
    st.stop()
      
else:
    if 'meta_data' not in response_analytics.json():
        st.write('No data provided by the API')
        st.stop()
    else:

        data = response_analytics.json()
        df_market_sentiment = pd.DataFrame(data['RETURNS_CALCULATIONS'])

# TODO: Not workign correctly. do not recieve any data from the API


# https://alphavantageapi.co/timeseries/analytics?SYMBOLS=MSFT,IBM,AAPL&RANGE=2023-07-03&RANGE=2023-08-31&INTERVAL=DAILY&OHLC=close&CALCULATIONS=MEAN,STDDEV,CORRELATION&apikey=demo
# https://alphavantageapi.co/timeseries/analytics?SYMBOLS=AAPL,MSFT,IBM&RANGE=2023-07-01&RANGE=2023-08-31&INTERVAL=DAILY&OHLC=close&CALCULATIONS=MEAN,STDDEV,CORRELATION&apikey=demo