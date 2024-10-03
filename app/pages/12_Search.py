import streamlit as st
import requests
import json
import pandas as pd


# Load the API key from the secret file
api_key = st.secrets["ALPHA_VABTAGE_API_KEY_demo"]

# Get user input for search text
search_text = st.text_input("Enter search text")

if search_text:
    
    # Download the CSV file
    search_url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={search_text}&apikey={api_key}'

    r = requests.get(search_url)
    # st.write(r.status_code)
    # st.write(search_url)
    # st.write(r.json())
    if r.status_code != 200:
        st.write('Error fetching data')
        st.stop()
        
    else:
        if 'bestMatches' not in r.json():
            st.write('No data provided by the API')
            st.stop()
        else:
            data = r.json()
            df_search = pd.DataFrame(data['bestMatches'])
            event = st.dataframe(df_search, selection_mode='single-row', on_select='rerun')

            # Catch the selection
            if event.selection:
                selected_row = event.selection['rows']
                st.write('You selected:', df_search.iloc[selected_row])
else:
    st.write('Please enter a search text')
