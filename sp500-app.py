import streamlit as st
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

st.title('S&P 500 App')

st.markdown('''
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
''')

st.header('User Input Feature')

# Web scraping of S&P 500 data
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    
    return df

df = load_data() 

# Sidebar - Sector selection
sorted_selected_unique = sorted( df['GICS Sector'].unique() )
selected_sorted = st.sidebar.multiselect('Sector', sorted_selected_unique, sorted_selected_unique)

# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sorted)) ]

st.header('Display Companies in Selected Sector')
st.write(f'Data Dimensions: {df_selected_sector.shape[0]} rows and {df_selected_sector.shape[1]} columns.')
st.dataframe(df_selected_sector)




