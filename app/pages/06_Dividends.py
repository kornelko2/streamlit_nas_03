import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

api_key = st.secrets["ALPHA_VABTAGE_API_KEY_demo"]

st.header('Basic Company Overview')
ticker = st.text_input('Enter a ticker', 'IBM')

url_dividends = f'https://www.alphavantage.co/query?function=DIVIDENDS&symbol={ticker}&apikey={api_key}'
response_dividends = requests.get(url_dividends)

if response_dividends.status_code != 200:
    st.write('Error fetching data')
    st.stop()
        
else:
    if 'data' not in response_dividends.json():
        st.write('No data provided by the API')
        st.stop()
    else:
        data = response_dividends.json()
        df_dividends = pd.DataFrame(data['data'])

st.write(df_dividends)

df_dividends['amount'] = pd.to_numeric(df_dividends['amount'])
df_dividends['ex_dividend_date'] = pd.to_datetime(df_dividends['ex_dividend_date'])

# st.write(df_dividends.dtypes)
# st.bar_chart(x=df_dividends['ex_dividend_date'], y=df_dividends['amount'])

# Reset the index of the dataframe
df_dividends.reset_index(inplace=True)

# Use the column names for x and y parameters
st.bar_chart(x='ex_dividend_date', y='amount', data=df_dividends)