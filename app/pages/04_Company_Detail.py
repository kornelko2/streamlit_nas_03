import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.title('Stock Detailed analysis')

# Fetch the list of S&P 500 tickers from Wikipedia

@st.cache_data
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url, header=0)
    df = table[0]
    return df['Symbol'].tolist()

sp500_tickers = get_sp500_tickers()

selected_tickers = st.selectbox('Select Stock Tickers', sp500_tickers)

company_info = []
for ticker in selected_tickers:
    info = yf.Ticker(ticker).info
    company_info.append(info)
    # Create a dataframe to store company info
    df_company_info = pd.DataFrame(company_info)     
    # Display the filtered dataframe
    st.write('Company Info:')
    st.write(company_info)
    balance_sheet = yf.Ticker(ticker).balance_sheet
    st.write(f'Balance Sheet for {ticker}:')
    st.write(balance_sheet)
    # Fetch the quarterly balance sheet data
    quarterly_balance_sheet = yf.Ticker(ticker).quarterly_balance_sheet
    st.write(f'Quarterly Balance Sheet for {ticker}:')
    st.write(quarterly_balance_sheet)
    # Fetch the cash flow statement data
    cash_flow = yf.Ticker(ticker).cashflow
    st.write(f'Cash Flow Statement for {ticker}:')
    st.write(cash_flow)
    # Fetch the quarterly cash flow statement data
    quarterly_cash_flow = yf.Ticker(ticker).quarterly_cashflow
    st.write(f'Quarterly Cash Flow Statement for {ticker}:')
    st.write(quarterly_cash_flow)
    # Fetch the income statement data
    income_statement = yf.Ticker(ticker).financials
    st.write(f'Income Statement for {ticker}:')
    st.write(income_statement)
    # Fetch the quarterly income statement data
    quarterly_income_statement = yf.Ticker(ticker).quarterly_financials
    st.write(f'Quarterly Income Statement for {ticker}:')
    st.write(quarterly_income_statement)
    # Fetch dividend data
    dividend_history = yf.Ticker(ticker).dividends
    st.write(f'Dividend History for {ticker}:')
    st.write(dividend_history)
    # Fetch the major holders data
    major_holders = yf.Ticker(ticker).major_holders
    st.write(f'Major Holders for {ticker}:')
    st.write(major_holders)
    # Fetch the insider transactions data
    insider_transactions = yf.Ticker(ticker).insider_transactions
    st.write(f'Insider Transactions for {ticker}:')
    st.write(insider_transactions)
    # Fetch the stock recommendation data
    recommendations = yf.Ticker(ticker).recommendations

    # Display the stock recommendation data
    st.write(f'Stock Recommendations for {ticker}:')
    st.write(recommendations)

    # Fetch the stock news
    news = yf.Ticker(ticker).news

    # Display the stock news
    st.write(f'Stock News for {ticker}:')
    st.write(news)
else:
    st.write("Please select at least one ticker.")
# Calculate the correlation matrix
