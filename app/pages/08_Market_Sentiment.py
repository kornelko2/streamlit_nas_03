import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

# market sentiment

api_key = st.secrets["ALPHA_VABTAGE_API_KEY_demo"]

st.header('Market Sentiment')
ticker = st.text_input('Enter a ticker', 'AAPL')

url_sentiment = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}'
response_market_sentiment = requests.get(url_sentiment)

# st.write(response_market_sentiment.json())

if response_market_sentiment.status_code != 200:
    st.write('Error fetching data')
    st.stop()
        
else:
    if 'feed' not in response_market_sentiment.json():
        st.write('No data provided by the API')
        st.stop()
    else:

        data = response_market_sentiment.json()
        df_market_sentiment = pd.DataFrame(data['feed'])

# st.write(response_market_sentiment.status_code)
# st.write(url_sentiment)

# st.write(data)



def create_articles(df_market_sentiment):
    col1, col2 = st.columns(2)
    for index, row in df_market_sentiment.iterrows():
        with col1 if index % 2 == 0 else col2:
            title = row['title'] if pd.notna(row['title']) else "No Title"
            banner_image = row['banner_image'] if pd.notna(row['banner_image']) else None
            authors = row['authors'] if pd.notna(row['authors']) else "Unknown"
            summary = row['summary'] if pd.notna(row['summary']) else "No Summary"
            url = row['url'] if pd.notna(row['url']) else "#"
            sentiment_score= row['overall_sentiment_score'] if pd.notna(row['overall_sentiment_score']) else "#"
            sentiment_label= row['overall_sentiment_label'] if pd.notna(row['overall_sentiment_label']) else "#"

            published = row['time_published'] if pd.notna(row['time_published']) else "Unknown"
            if published != "Unknown":
                try:
                    published_datetime = datetime.strptime(published, "%Y%m%dT%H%M%S")
                    published = published_datetime.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    published = "Invalid date format"
            st.subheader(title)
            if banner_image:
                st.image(banner_image, caption=row['source'])
            st.write(f"**Published on {published}**")
            st.write(f"**Sent. Score: {sentiment_score}**")
            st.write(f"**Sent. Label: {sentiment_label}**")
            st.markdown(f"**by {authors}**<br>{summary}<br>({url})", unsafe_allow_html=True)
            st.markdown('---')  # Add a horizontal line between articles

# Display articles
create_articles(df_market_sentiment)