from stocksymbol import StockSymbol
import yaml
import pickle
import time
import streamlit as st
from pathlib import Path


def load_tickers(market, api_key):
    ticker_filename = 'app/data/' + market + '_tickers'
    ticker_file_path = Path(ticker_filename)
    if ticker_file_path.is_file():
        with open(ticker_filename, 'rb') as f:
            mylist = pickle.load(f)
            return mylist
    else:
        st.write('File not found...Downloading')
        download_and_save_tickers(api_key, market)
        st.write(f'Successful download tickers file for {market}')
        mylist = load_tickers(market, api_key)
        return mylist

def download_and_save_tickers(api_key, market):

    ss = StockSymbol(api_key)
    symbol_only_list = ss.get_symbol_list(market=market, symbols_only=True)
    ticker_filename = 'app/data/' + market+'_tickers'
    with open(ticker_filename, 'wb') as f:
        pickle.dump(symbol_only_list, f)

    return 'Successful'
