# let us use onlz the official documentation for steamlit
# https://docs.streamlit.io/en/stable/api.html

import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots



# Load the API key from the secret file
api_key = st.secrets["ALPHA_VABTAGE_API_KEY_demo"]



# Download the CSV file
csv_url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}'


# Make the REST call to Alpha Vantage


# Define a function to fetch the data
@st.cache_data
def fetch_and_clean_data(csv_url):

    df_ticker = pd.read_csv(csv_url)
    
    return df_ticker


# Fetch the data
df_ticker = fetch_and_clean_data(csv_url)

# Create a searchable dropdown menu with combined columns
df_ticker['combined'] = df_ticker.apply(lambda row: f"{row['symbol']} - {row['name']} - {row['exchange']}", axis=1)
selected_symbol = st.selectbox('Select a symbol', df_ticker['combined'].drop_duplicates().reset_index(drop=True))
# Extract the symbol from the selected dropdown value
symbol = selected_symbol.split(' - ')[0]

# Display the filtered dataframe
st.write(symbol)

url_daily = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
url_weekly = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={api_key}'

@st.cache_data
def fetch_and_clean_timeline_data(url_daily, url_weekly):
    response_daily = requests.get(url_daily)
    if response_daily.status_code != 200:
        st.write('Error fetching data')
        st.stop()
    else:
        
        if 'Meta Data' not in response_daily.json():
            st.write('No data provided by the API')
            st.stop()
        else:
            # Parse the response
            data_daily = json.loads(response_daily.text)
            # Convert the data into a dataframe
            df_daily = pd.DataFrame(data_daily['Time Series (Daily)']).T

            response_weekly = requests.get(url_weekly)
            # Parse the response
            data_weekly = json.loads(response_weekly.text)
            # Convert the data into a dataframe
            df_weekly = pd.DataFrame(data_weekly['Weekly Time Series']).T

            return df_daily, df_weekly 

df_timeline_daily, df_timeline_weekly = fetch_and_clean_timeline_data(url_daily, url_weekly)

daily_weekly_selector = st.radio('Select the timeline', ['Daily', 'Weekly'])
st.write(daily_weekly_selector)

if daily_weekly_selector == "Daily":
    df_timeline = df_timeline_daily
else:
    df_timeline = df_timeline_weekly

# Create the financial timeline figure
fig = make_subplots(rows=2, cols=1, 
                    shared_xaxes=True, 
                    vertical_spacing=0.02, 
                    subplot_titles=('Candlestick', 'Volume'),
                    row_heights=[0.8, 0.2])

# Add the open, high, low, and close traces
fig.add_trace(go.Candlestick(x=df_timeline.index, 
                             open=df_timeline['1. open'], 
                             high=df_timeline['2. high'], 
                             low=df_timeline['3. low'], 
                             close=df_timeline['4. close'],
                             name='Price', 
                             increasing_line_color='green', 
                             decreasing_line_color='red'), 
                             row=1, col=1)


# Create the volume subplot
fig.add_trace(go.Bar(x=df_timeline.index, 
                     y=df_timeline['5. volume'], 
                     name='Volume'), 
                     row=2, col=1)

fig.update_layout(title='Candlestick and Volume Chart',
                  yaxis_title='Stock Price',
                  yaxis2_title='Volume',
                  xaxis_rangeslider_visible=False)

# Display the figure in Streamlit
st.plotly_chart(fig)

# Display the data in Streamlit
