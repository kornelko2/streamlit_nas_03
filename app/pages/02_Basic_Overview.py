import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

api_key = st.secrets["ALPHA_VABTAGE_API_KEY_demo"]

st.header('Basic Company Overview')
ticker = st.text_input('Enter a ticker', 'IBM')
url_company_overview = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}'
response_company_overview = requests.get(url_company_overview)

if response_company_overview.status_code != 200:
    st.write('Error fetching data')
    st.stop()
      
else:
    if 'Symbol' not in response_company_overview.json():
        st.write('No data provided by the API')
        st.stop()
    else:

        data = response_company_overview.json()
        df_company_overview = pd.DataFrame.from_dict(data, orient='index').T


# st.write(df_company_overview)
st.subheader(f"Ticker: {df_company_overview['Symbol'].values[0]}")
st.write(f"Name: {df_company_overview['Name'].values[0]}")
st.write(f"Description: {df_company_overview['Description'].values[0]}")

# Define the keys to display
keys = ['Exchange', 'Currency', 'Country', 'Sector', 'Industry', 'Address', 'OfficialSite']
keys2 = df_company_overview.columns.tolist()
keys2 = keys2[4:]
# st.write(keys2)

cols = st.columns(2)
for i, key in enumerate(keys2):
            col = cols[i % 2]
            with col:
                st.markdown(
                    f"""
                    <strong>{key}</strong>: {df_company_overview[key].values[0]}
                    """,
                    unsafe_allow_html=True
                )