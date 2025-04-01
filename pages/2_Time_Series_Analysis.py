import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose

# Page Configuration
st.set_page_config(page_title="Time Series Analysis", layout="wide")

# Sidebar Inputs
st.sidebar.header("Time Series Analysis")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Custom CSS for Justifying Text
st.markdown("""
    <style>
    .justified-text {
        text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

# Fetch Stock Data
if stock_symbol:
    try:
        stock = yf.Ticker(stock_symbol)
        df = stock.history(start=start_date, end=end_date)
        df.reset_index(inplace=True)

        st.title(f"📊 Time Series Analysis for {stock_symbol.upper()}")

        # 📈 Closing Price Over Time
        st.subheader("Closing Price Over Time")
        st.markdown(
            '<div class="justified-text">This plot shows the historical trend of the closing price of the selected stock over time. '
            'It helps in identifying long-term trends and patterns, such as uptrends, downtrends, and consolidations.</div>',
            unsafe_allow_html=True)
        fig_close = px.line(df, x="Date", y="Close", labels={"Close": "Closing Price (USD)"})
        st.plotly_chart(fig_close, use_container_width=True)

        # 📊 Volume Traded Over Time
        st.subheader("Volume Traded Over Time")
        st.markdown(
            '<div class="justified-text">This bar chart represents the number of shares traded daily. A sudden increase in volume '
            'may indicate strong investor interest and potential price movement.</div>',
            unsafe_allow_html=True)
        fig_volume = px.bar(df, x="Date", y="Volume", labels={"Volume": "Volume Traded"})
        st.plotly_chart(fig_volume, use_container_width=True)

        # Opening vs Closing Prices Over Time
        st.subheader("Opening vs Closing Prices Over Time")
        st.markdown(
            '<div class="justified-text">This graph compares the stock’s opening and closing prices each day. A significant '
            'difference between them may indicate high volatility and investor reactions to market news.</div>',
            unsafe_allow_html=True)
        fig_open_close = go.Figure()
        fig_open_close.add_trace(go.Scatter(x=df["Date"], y=df["Open"], mode="lines", name="Opening Price"))
        fig_open_close.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name="Closing Price"))
        fig_open_close.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
        st.plotly_chart(fig_open_close, use_container_width=True)

        # Time Series Decomposition
        st.subheader("Time Series Decomposition")
        st.markdown(
            '<div class="justified-text">Time series decomposition breaks down the stock price into trend, seasonal, and residual '
            'components. The trend shows the long-term movement, the seasonal component captures periodic patterns, and the residual '
            'reveals unexplained fluctuations.</div>',
            unsafe_allow_html=True)
        decomposition = seasonal_decompose(df['Close'].dropna(), model='multiplicative', period=30)
        fig_decomp = go.Figure()
        fig_decomp.add_trace(go.Scatter(x=df['Date'], y=decomposition.trend, mode='lines', name='Trend'))
        fig_decomp.add_trace(go.Scatter(x=df['Date'], y=decomposition.seasonal, mode='lines', name='Seasonal'))
        fig_decomp.add_trace(go.Scatter(x=df['Date'], y=decomposition.resid, mode='lines', name='Residual'))
        fig_decomp.update_layout(height=600)
        st.plotly_chart(fig_decomp, use_container_width=True)

        # Candlestick Chart (OHLC)
        st.subheader("OHLC Chart (Candlestick Chart)")
        st.markdown(
            '<div class="justified-text">The candlestick chart represents the stock’s price movements for each day. The wicks '
            'show the highest and lowest prices, while the body indicates the opening and closing prices. It helps in understanding '
            'market sentiment and trend reversals.</div>',
            unsafe_allow_html=True)
        fig_candlestick = go.Figure(data=[go.Candlestick(x=df['Date'],
                                                    open=df['Open'],
                                                    high=df['High'],
                                                    low=df['Low'],
                                                    close=df['Close'])])
        st.plotly_chart(fig_candlestick, use_container_width=True)

    except Exception as e:
        st.error(f"Error fetching data for {stock_symbol.upper()}. Please check the symbol and try again.")
