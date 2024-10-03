import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime


# Load the API key from the secret file
api_key = st.secrets["ALPHA_VABTAGE_API_KEY_demo"]

url = 'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=demo'
response_market_status = requests.get(url)
data = response_market_status.json()
df_market_status = pd.DataFrame(data['markets'])

st.write(df_market_status)

