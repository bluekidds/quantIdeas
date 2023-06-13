import streamlit as st

import yaml

from glob import glob
import ffn
from stocksymbol import StockSymbol
from data_utils import download_and_save_tickers, load_tickers
from datetime import date

today = date.today()

def get_data_filename(directory='app/data'):
    file_list = glob(directory+'/*')
    available_market_list = [f.split('/')[-1] for f in file_list]
    return available_market_list


with open('app/resource.yaml', 'r') as file:
    resources = yaml.safe_load(file)

api_key = resources['tickers']['api_key']

ss = StockSymbol(api_key)
markets = ss.market_list
market_list = [d['market'] for d in markets]

st.title('Stock Quant FFN Demo')

with st.expander('Store or retrieve ticker'):
    with st.sidebar:
        market_name = st.selectbox('Select the Market', market_list)
        store_or_retrieve = st.radio(
            "Save or Load the tickers",
            ('None', 'Save', 'Load'))

        if store_or_retrieve == 'Save':
            result = download_and_save_tickers(api_key, market_name)

        elif store_or_retrieve == 'Load':
            ticker_list = load_tickers(market_name, api_key)
            st.write(f"Load total {len(ticker_list)} tickers")


with st.expander("Select a stock to analyze"):
    file_list = get_data_filename()

    market_name = st.selectbox('Select the file name', file_list).split('_')[0]
    ticker_list = load_tickers(market_name, api_key)
    tickers = st.multiselect("Select stocks to compare", ticker_list)

if st.button('Analyze'):

    data = ffn.get(tickers, start='2010-01-01', end=today)

    st.dataframe(data.head())

    returns = data.to_log_returns().dropna()

    ax = returns.plot_corr_heatmap()

    st.pyplot(ax)

    ax2 = data.rebase().plot(figsize=(12, 5))

    st.pyplot(ax)
    st.markdown('### Analyze Performance')
    perf = data.calc_stats()



    st.write(returns.calc_mean_var_weights().as_format('.2%'))


