import streamlit as st
import pandas as pd
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Comparative & Statistical Analysis", layout="wide")

# Sidebar Inputs for Stock Symbol(s) and Date Range
st.sidebar.header("Stock Comparison")
symbols_input = st.sidebar.text_input("Enter Stock Symbols (comma separated, e.g., AAPL, MSFT, GOOGL)", "AAPL, MSFT, GOOGL")
symbols_list = [symbol.strip() for symbol in symbols_input.split(',')]
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Function to fetch stock data
def load_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data

st.title("⚖️ Comparative and Statistical Analysis")
# Comparative Closing Prices Plot
st.subheader("Comparative Closing Prices")
fig_compare = go.Figure()
for symbol in symbols_list:
    try:
        compare_data = load_data(symbol, start_date, end_date)
        fig_compare.add_trace(go.Scatter(x=compare_data['Date'], y=compare_data['Close'], mode='lines', name=symbol))
    except Exception as e:
        st.write(f"Could not fetch data for {symbol}: {e}")

fig_compare.update_layout(xaxis_title="Date", yaxis_title="Closing Price (USD)")
st.plotly_chart(fig_compare, use_container_width=True)


# Histogram of Returns
st.subheader("Histogram of Returns")
returns = pd.DataFrame()
for symbol in symbols_list:
    try:
        # Fetch data for each symbol
        stock_data = load_data(symbol, start_date, end_date)
        stock_data['Daily Return'] = stock_data['Close'].pct_change()
        returns[symbol] = stock_data['Daily Return']

    except Exception as e:
        st.write(f"Could not fetch data for {symbol}: {e}")

# Plot histogram
fig_hist = px.histogram(returns, x=returns.columns, nbins=50, labels={"value": "Daily Return"})
fig_hist.update_layout(barmode='overlay')
fig_hist.update_traces(opacity=0.75)
st.plotly_chart(fig_hist, use_container_width=True)