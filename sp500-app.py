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

# Download S&P500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance/
data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Symbol
def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    fig, ax = plt.subplots()
    ax.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
    ax.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
    ax.tick_params(axis='x', rotation=90)
    ax.set_title(symbol, fontweight='bold')
    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Closing Price', fontweight='bold')
    return st.pyplot(fig)

num_company = st.sidebar.slider('Number of Companies', 1, 10)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:int(num_company)]:
        price_plot(i)
