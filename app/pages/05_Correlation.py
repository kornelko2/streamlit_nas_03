import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import plotly.express as px


st.title('Stock portfolio correlation analysis')

# Fetch the list of S&P 500 tickers from Wikipedia
@st.cache_data
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url, header=0)
    df = table[0]
    return df['Symbol'].tolist()

all_tickers = get_sp500_tickers()

selected_tickers = st.multiselect('Select Stock Tickers', all_tickers) 
start_date = st.date_input('Select Start Date', value=datetime(2022,1,1)) 
end_date = st.date_input('Select End Date', value=datetime(2022,12,31))

if selected_tickers:
    # Fetch the historical stock data
    data = yf.download(selected_tickers, start=start_date, end=end_date)['Close']
    
    company_info = []
    for ticker in selected_tickers:
        info = yf.Ticker(ticker).info
        company_info.append(info)
    # Create a dataframe to store company info
    df_company_info = pd.DataFrame(company_info)
    
    # Display the dataframe
    
    # Select the columns to display in the company info table
    columns_to_display = ['symbol', 'shortName', 'sector', 'industry']

    # Filter the dataframe to include only the selected columns
    df_company_info_filtered = df_company_info[columns_to_display]

    # Display the filtered dataframe
    st.write('Company Info:')
    st.write(df_company_info_filtered)
    
    if len(selected_tickers) >= 2:
        # Calculate the correlation matrix
        correlation_matrix = data.corr(method='pearson')
        st.write('Correlation Matrix:')
        st.write(correlation_matrix)

        # Create a heatmap of the correlation matrix
        st.write('Correlation Heatmap:')
        fig = px.imshow(correlation_matrix, color_continuous_scale='RdBu')
        st.plotly_chart(fig)
    else:
        st.write("Please select at least two tickers to calculate correlation.")
    # Calculate the correlation matrix
 
else:
    st.write("Please select at least one ticker.")
