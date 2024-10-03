import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from pygwalker.api.streamlit import StreamlitRenderer

st.set_page_config(
    page_title="Income Statement",
    layout="wide"
)

api_key = st.secrets["ALPHA_VABTAGE_API_KEY_demo"]

st.header('Income Statement')
ticker = st.text_input('Enter a ticker', 'IBM')

url_income_statement = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={api_key}'
url_balance_sheet = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={api_key}'
url_cash_flow = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={api_key}'
url_earnings = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={api_key}'


response_income_statement = requests.get(url_income_statement)
response_balance_sheet = requests.get(url_balance_sheet)
response_cash_flow = requests.get(url_cash_flow)

data_income_statement  = response_income_statement.json()
data_balance_sheet  = response_balance_sheet.json()
data_cash_flow  = response_cash_flow.json()

if response_income_statement.status_code != 200:
    st.write('Error fetching data')
    st.stop()
        
else:
    if 'symbol' not in response_income_statement.json():
        st.write('No data provided by the API')
        st.stop()
    else:

        df_income_statement_annual = pd.DataFrame(data_income_statement ['annualReports'])
        df_income_statement_quarterly = pd.DataFrame(data_income_statement ['quarterlyReports'])

        df_balance_sheet_annual = pd.DataFrame(data_balance_sheet ['annualReports'])
        df_balance_sheet_quarterly = pd.DataFrame(data_balance_sheet ['quarterlyReports'])

        df_cash_flow_annual = pd.DataFrame(data_cash_flow ['annualReports'])
        df_cash_flow_quarterly = pd.DataFrame(data_cash_flow ['quarterlyReports'])


# selector
annual_quarterly_selector = st.radio('Select the timeline', ['Annual', 'Quarterly'])
st.write(annual_quarterly_selector)

if annual_quarterly_selector == "Annual":
    df_income_statement = df_income_statement_annual
    df_balance_sheet = df_balance_sheet_annual
    df_cash_flow = df_cash_flow_annual
else:
    df_income_statement = df_income_statement_quarterly
    df_balance_sheet = df_balance_sheet_quarterly
    df_cash_flow = df_cash_flow_quarterly

st.write(df_income_statement)
st.write(df_balance_sheet)
st.write(df_cash_flow)


# Create Plots

fig = make_subplots(rows=2, cols=3, 
                    shared_xaxes=True, 
                    subplot_titles=('Income', 'Costs', 'Interest', "EBIT/EBITDA"),
                    )

fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['grossProfit'], 
                     name='Gross Profit'), 
                     row=1, col=1)
fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['totalRevenue'], 
                     name='Total Revenue'), 
                     row=1, col=1)

fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['netIncome'], 
                     name='Net Income'), 
                     row=1, col=1)

fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['costOfRevenue'], 
                     name='Cost of Revenue'), 
                     row=1, col=2)
fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['costofGoodsAndServicesSold'], 
                     name='Cost of Goods and Services Sold'), 
                     row=1, col=2)
fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['researchAndDevelopment'], 
                     name='Research and Development'), 
                     row=1, col=2)
fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['operatingExpenses'], 
                     name='Operating Expenses'), 
                     row=1, col=2)

fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['netInterestIncome'], 
                     name='Net Interest Income'), 
                     row=1, col=3)
fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['interestIncome'], 
                     name='Interest Income'), 
                     row=1, col=3)
fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['interestExpense'], 
                     name='Interest Expense'), 
                     row=1, col=3)
fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['ebit'], 
                     name='EBIT'), 
                     row=2, col=1)
fig.add_trace(go.Bar(x=df_income_statement['fiscalDateEnding'], 
                     y=df_income_statement['ebitda'], 
                     name='EBITDA'), 
                     row=2, col=1)

fig.update_layout(title='Candlestick and Volume Chart',
                  yaxis_title='Stock Price',
                  yaxis2_title='Volume',
                  xaxis_rangeslider_visible=False,
                  xaxis=dict(autorange='reversed'))

# Display the figure in Streamlit
st.plotly_chart(fig)

# pyg_app = StreamlitRenderer(df_income_statement_annual)
 
# pyg_app.explorer()
