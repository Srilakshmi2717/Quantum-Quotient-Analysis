import streamlit as st
import pandas as pd
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Set Page Configuration
st.set_page_config(page_title="Technical Indicators & Trend Analysis", layout="wide")

# Sidebar Navigation for Subpages
st.sidebar.header("Technical Indicators & Trend Analysis")
subpage = st.sidebar.radio(
    "Select an Indicator Category",
    [
        "Price Trend & Moving Averages",
        "Volatility & Risk Metrics",
        "Momentum & Overbought/Oversold Indicators",
        "Volume-Based Indicators",
        "Support, Resistance & Channel-Based Indicators",
        "Trade & Market Behavior Analysis"
    ]
)

# Main Content Based on Subpage Selection
if subpage == "Price Trend & Moving Averages":
    st.title("📊 Price Trend & Moving Averages")
    st.write("""
    - **Simple Moving Average (SMA)**  
    - **Exponential Moving Average (EMA)**  
    - **VWAP (Volume-Weighted Average Price) Over Time**  
    - **MACD Indicator (Trend & Momentum)**  
    """)

    # Sidebar Inputs for Stock Symbol, Start Date, End Date
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

    # Fetch Stock Data
    if stock_symbol:
        try:
            stock = yf.Ticker(stock_symbol)
            df = stock.history(start=start_date, end=end_date)
            df.reset_index(inplace=True)

            # Add Simple Moving Average (SMA)
            st.subheader("Simple Moving Average (SMA)")
            sma_period = st.slider("Select SMA Period", min_value=5, max_value=200, value=50)
            df['SMA'] = df['Close'].rolling(window=sma_period).mean()
            st.markdown(
                """
                The **Simple Moving Average (SMA)** is a commonly used indicator that smoothens price data by creating a constantly updated average price over a specific period. The line represents the average price over a given period, which helps traders identify trends and reversals in the market. A longer period SMA reacts slower to price changes, whereas a shorter period SMA is more sensitive.
                """, 
                unsafe_allow_html=True
            )
            # Plotting SMA
            fig_sma = go.Figure()
            fig_sma.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name="Closing Price", line=dict(color='darkcyan')))
            fig_sma.add_trace(go.Scatter(x=df['Date'], y=df['SMA'], mode='lines', name=f"SMA {sma_period}", line=dict(color='crimson')))
            fig_sma.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig_sma, use_container_width=True)

            # Add Exponential Moving Average (EMA)
            st.subheader("Exponential Moving Average (EMA)")
            ema_period = st.slider("Select EMA Period", min_value=5, max_value=200, value=50)
            df['EMA'] = df['Close'].ewm(span=ema_period, adjust=False).mean()
            st.markdown(
                """
                The **Exponential Moving Average (EMA)** is similar to the SMA but gives more weight to recent prices, making it more responsive to new information. EMAs are more useful than SMAs for short-term trading, as they react more quickly to price changes. When the price is above the EMA, the market is typically in an uptrend.
                """, 
                unsafe_allow_html=True
            )
            # Plotting EMA
            fig_ema = go.Figure()
            fig_ema.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name="Closing Price", line=dict(color='darkcyan')))
            fig_ema.add_trace(go.Scatter(x=df['Date'], y=df['EMA'], mode='lines', name=f"EMA {ema_period}", line=dict(color='crimson')))
            fig_ema.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig_ema, use_container_width=True)

            # Add VWAP (Volume-Weighted Average Price)
            st.subheader("VWAP (Volume-Weighted Average Price)")
            df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
            st.markdown(
                """
                **VWAP (Volume-Weighted Average Price)** is an important indicator used by traders to measure the average price a security has traded at throughout the day, based on both volume and price. It’s a great indicator for assessing the overall trend of a stock throughout the trading day. VWAP is commonly used to gauge the efficiency of a trade.
                """, 
                unsafe_allow_html=True
            )
            # Plotting VWAP
            fig_vwap = go.Figure()
            fig_vwap.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name="Closing Price", line=dict(color='darkcyan')))
            fig_vwap.add_trace(go.Scatter(x=df['Date'], y=df['VWAP'], mode='lines', name="VWAP", line=dict(dash='dot', color='crimson')))
            fig_vwap.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig_vwap, use_container_width=True)

            # Add MACD (Moving Average Convergence Divergence)
            st.subheader("📉 MACD Indicator (Trend & Momentum)")
            df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
            df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = df['EMA_12'] - df['EMA_26']
            df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
            st.markdown(
                """
                The **MACD (Moving Average Convergence Divergence)** is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. The MACD is calculated by subtracting the 26-period EMA from the 12-period EMA. The signal line is the 9-period EMA of the MACD. The MACD can help identify potential buy and sell signals.
                """, 
                unsafe_allow_html=True
            )
            # Plotting MACD
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], mode='lines', name="MACD", line=dict(color='darkcyan')))
            fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['Signal_Line'], mode='lines', name="Signal Line", line=dict(color='crimson')))
            fig_macd.update_layout(xaxis_title="Date", yaxis_title="MACD")
            st.plotly_chart(fig_macd, use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching data for {stock_symbol.upper()}. Please check the symbol and try again.")


elif subpage == "Volatility & Risk Metrics":
    st.title("📈 Volatility & Risk Metrics")
    st.write("""
    - **Annualized Volatility**  
    - **Average True Range (ATR)**  
    - **Ulcer Index (Risk Indicator)**  
    """)

    # Sidebar Inputs for Stock Symbol and Date Range
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

    # Fetch Stock Data
    if stock_symbol:
        try:
            stock = yf.Ticker(stock_symbol)
            df = stock.history(start=start_date, end=end_date)
            df.reset_index(inplace=True)

            # Annualized Volatility
            st.subheader("Annualized Volatility")
            st.write("""
            **Annualized Volatility** is a measure of how much the stock price fluctuates over the course of a year. It is calculated
            by multiplying the standard deviation of daily returns by the square root of 252 (the number of trading days in a year).
            A higher volatility indicates higher risk.
            """)
            df['daily_return'] = df['Close'].pct_change()
            annualized_volatility = df['daily_return'].std() * np.sqrt(252)  # 252 trading days
            st.write(f"**Annualized Volatility**: {annualized_volatility:.2%}")
            # Plot: Annualized Volatility (rolling 30 days)
            fig_volatility = px.line(df, x="Date", y=df['daily_return'].rolling(window=30).std() * np.sqrt(252),
                                     labels={"value": "Annualized Volatility", "Date": "Date"})
            fig_volatility.update_traces(line=dict(color='goldenrod'))  
            st.plotly_chart(fig_volatility, use_container_width=True)

            # Average True Range (ATR)
            st.subheader("Average True Range (ATR)")
            df['TR'] = np.maximum(df['High'] - df['Low'], np.abs(df['High'] - df['Close'].shift(1)), np.abs(df['Low'] - df['Close'].shift(1)))
            df['ATR'] = df['TR'].rolling(window=14).mean()
            st.write("""
            **Average True Range (ATR)** is a volatility indicator that measures market volatility by decomposing the entire range
            of an asset for that period. It is the average of the true ranges over a specified period (typically 14 days).
            ATR helps to understand price movement and potential risk.
            """)
            # Plot: ATR
            fig_atr = px.line(df, x="Date", y="ATR", labels={"ATR": "Average True Range (ATR)", "Date": "Date"})
            fig_atr.update_traces(line=dict(color='goldenrod'))  
            st.plotly_chart(fig_atr, use_container_width=True)

            # Ulcer Index (Risk Indicator)
            st.subheader("Ulcer Index (Risk Indicator)")
            df['drawdown'] = df['Close'] / df['Close'].cummax() - 1
            df['ulcer_index'] = np.sqrt((df['drawdown'] ** 2).rolling(window=14).mean())
            st.write("""
            **Ulcer Index (Risk Indicator)** is a risk metric that focuses on the severity and duration of drawdowns. 
            It calculates the square root of the average squared drawdown over a given period. The higher the Ulcer Index, 
            the higher the risk (as it indicates a greater decline in asset value from its peak).
            """)
            # Plot: Ulcer Index
            fig_ulcer = px.line(df, x="Date", y="ulcer_index", labels={"ulcer_index": "Ulcer Index (Risk Indicator)", "Date": "Date"})
            fig_ulcer.update_traces(line=dict(color='goldenrod'))  
            st.plotly_chart(fig_ulcer, use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching data for {stock_symbol.upper()}. Please check the symbol and try again.\n\n{e}")


elif subpage == "Momentum & Overbought/Oversold Indicators":
    st.title("📉 Momentum & Overbought/Oversold Indicators")
    st.write("""
    - **Relative Strength Index (RSI) Chart**  
    - **Stochastic Oscillator**  
    - **Fisher Transform**  
    """)

    # Sidebar Inputs for Stock Symbol and Date Range
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

    # Fetch Stock Data
    if stock_symbol:
        try:
            stock = yf.Ticker(stock_symbol)
            df = stock.history(start=start_date, end=end_date)
            df.reset_index(inplace=True)

            # Relative Strength Index (RSI) Chart
            st.subheader("Relative Strength Index (RSI) Chart")
            delta = df['Close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            df['RSI'] = rsi
            st.write("""
            **Relative Strength Index (RSI)** is a momentum oscillator that measures the speed and change of price movements.
            RSI is typically used to identify overbought (>70) or oversold (<30) conditions in a stock. A high RSI suggests
            that a stock is overbought and might be due for a pullback, while a low RSI suggests that it is oversold and
            may be due for a reversal.
            """)
            # Plot: RSI Chart
            fig_rsi = px.line(df, x="Date", y="RSI", labels={"RSI": "Relative Strength Index (RSI)", "Date": "Date"})
            fig_rsi.update_traces(line=dict(color='hotpink'))              
            st.plotly_chart(fig_rsi, use_container_width=True)

            # Stochastic Oscillator
            st.subheader("Stochastic Oscillator")
            # Calculate the Stochastic Oscillator %K and %D
            df['14-high'] = df['High'].rolling(window=14).max()
            df['14-low'] = df['Low'].rolling(window=14).min()
            df['%K'] = 100 * (df['Close'] - df['14-low']) / (df['14-high'] - df['14-low'])
            df['%D'] = df['%K'].rolling(window=3).mean()
            st.write("""
            The **Stochastic Oscillator** is a momentum indicator that compares a security's closing price to its price range 
            over a given time period. The %K line measures the current closing price in relation to the range, and the %D line
            is a 3-period moving average of %K. When %K crosses above %D, it indicates upward momentum, and when %K crosses below %D,
            it indicates downward momentum.
            """)
            # Plot: Stochastic Oscillator
            fig_stochastic = go.Figure()
            fig_stochastic.add_trace(go.Scatter(x=df['Date'], y=df['%K'], mode='lines', name='%K', line=dict(color='hotpink')))
            fig_stochastic.add_trace(go.Scatter(x=df['Date'], y=df['%D'], mode='lines', name='%D', line=dict(color='lightsalmon')))
            fig_stochastic.update_layout(xaxis_title="Date",
                                         yaxis_title="Stochastic Value",
                                         yaxis_range=[0, 100])
            st.plotly_chart(fig_stochastic, use_container_width=True)

            # Fisher Transform
            st.subheader("Fisher Transform")
            # Calculate the Fisher Transform
            df['max_close'] = df['Close'].rolling(window=10).max()
            df['min_close'] = df['Close'].rolling(window=10).min()
            df['value'] = 2 * ((df['Close'] - df['min_close']) / (df['max_close'] - df['min_close']) - 0.5)
            df['Fisher'] = 0.5 * np.log((1 + df['value']) / (1 - df['value']))
            st.write("""
            The **Fisher Transform** is a technical analysis indicator that converts prices into a Gaussian normal distribution.
            It is designed to identify turning points in the market by measuring the deviation of the price from a defined price range.
            Positive values indicate upward momentum, while negative values suggest downward momentum.
            """)
            fig_fisher = go.Figure()
            fig_fisher.add_trace(go.Scatter(x=df['Date'], y=df['Fisher'], mode='lines', 
                                        name="Fisher Transform", line=dict(width=2, color="hotpink")))
            fig_fisher.update_layout(
                xaxis_title="Date",
                yaxis_title="Fisher Value",
                yaxis_range=[df['Fisher'].min() - 1, df['Fisher'].max() + 1],  # Set y-axis range to add some padding
                template="plotly_dark"  
            )
            st.plotly_chart(fig_fisher, use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching data for {stock_symbol.upper()}. Please check the symbol and try again.\n\n{e}")

elif subpage == "Volume-Based Indicators":
    st.title("📊 Volume-Based Indicators")
    st.write("""
    - **On-Balance Volume (OBV)**  
    - **Intraday Intensity Index (IIX)**  
    - **Chaikin Money Flow (CMF)**  
    """)
    
    # Sidebar Inputs
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

    # Fetch Stock Data
    if stock_symbol:
        try:
            stock = yf.Ticker(stock_symbol)
            df = stock.history(start=start_date, end=end_date)
            df.reset_index(inplace=True)

            # Plot for OBV (On-Balance Volume)
            df['OBV'] = (df['Close'].diff().gt(0) * 2 - 1) * df['Volume']
            df['OBV'] = df['OBV'].cumsum()
            st.write("""
            **On-Balance Volume (OBV)**  
            OBV uses volume flow to predict changes in stock price. It is a cumulative indicator where volume is added on up days and subtracted on down days. A rising OBV indicates buying pressure, while a falling OBV indicates selling pressure.
            """)
            fig_obv = go.Figure()
            fig_obv.add_trace(go.Scatter(x=df['Date'], y=df['OBV'], mode='lines', name="On-Balance Volume", line=dict(color='limegreen', width=2)))
            fig_obv.update_layout(xaxis_title="Date", yaxis_title="OBV Value", template="plotly_dark")
            st.plotly_chart(fig_obv, use_container_width=True)

            # Plot for IIX (Intraday Intensity Index)
            df['IIX'] = ((df['Close'] - df['Low']) / (df['High'] - df['Low'])) * df['Volume']
            df['IIX'] = df['IIX'].rolling(window=14).mean()  # Moving Average of IIX for smoothing
            st.write("""
            **Intraday Intensity Index (IIX)**  
            The Intraday Intensity Index measures the strength of price movement based on volume. A higher IIX value indicates stronger buying interest, while a lower value indicates weaker buying or selling activity.
            """)
            fig_iix = go.Figure()
            fig_iix.add_trace(go.Scatter(x=df['Date'], y=df['IIX'], mode='lines', name="Intraday Intensity Index", line=dict(color='limegreen', width=2)))
            fig_iix.update_layout(xaxis_title="Date", yaxis_title="IIX Value", template="plotly_dark")
            st.plotly_chart(fig_iix, use_container_width=True)

            # Plot for CMF (Chaikin Money Flow)
            df['MFV'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low']) * df['Volume']
            df['CMF'] = df['MFV'].rolling(window=20).sum() / df['Volume'].rolling(window=20).sum()
            st.write("""
            **Chaikin Money Flow (CMF)**  
            The Chaikin Money Flow indicator measures the amount of Money Flow Volume over a specific period. It combines both price and volume to evaluate buying and selling pressure. A positive CMF indicates buying pressure, while a negative CMF suggests selling pressure.
            """)
            fig_cmf = go.Figure()
            fig_cmf.add_trace(go.Scatter(x=df['Date'], y=df['CMF'], mode='lines', name="Chaikin Money Flow", line=dict(color='limegreen', width=2)))
            fig_cmf.update_layout(xaxis_title="Date", yaxis_title="CMF Value", template="plotly_dark")
            st.plotly_chart(fig_cmf, use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching data for {stock_symbol.upper()}. Please check the symbol and try again.")

elif subpage == "Support, Resistance & Channel-Based Indicators":
    st.title("📉 Support, Resistance & Channel-Based Indicators")
    st.write("""
    - **Bollinger Bands**  
    - **Keltner Channel**  
    - **Donchian Channels**  
    """)

    # Sidebar Inputs for Stock Symbol and Date Range
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

    # Fetch Stock Data
    if stock_symbol:
        try:
            stock = yf.Ticker(stock_symbol)
            df = stock.history(start=start_date, end=end_date)
            df.reset_index(inplace=True)

            # Bollinger Bands
            st.subheader("Bollinger Bands")
            window = 20  # Bollinger Bands typically use a 20-day moving average
            df['SMA'] = df['Close'].rolling(window=window).mean()  # Simple Moving Average (SMA)
            df['upper_band'] = df['SMA'] + 2 * df['Close'].rolling(window=window).std()  # Upper Bollinger Band
            df['lower_band'] = df['SMA'] - 2 * df['Close'].rolling(window=window).std()  # Lower Bollinger Band
            st.write("""
            **Bollinger Bands** help identify periods of high and low volatility in the market. The upper and lower bands are set typically 2 standard deviations away from the simple moving average (SMA). The space between the bands can be used to gauge market conditions, with price often moving back toward the middle band after touching the outer bands.
            """)
            fig_bollinger = go.Figure()
            fig_bollinger.add_trace(go.Scatter(x=df['Date'], y=df['SMA'], mode='lines', name="SMA", line=dict(color='purple')))
            fig_bollinger.add_trace(go.Scatter(x=df['Date'], y=df['upper_band'], mode='lines', name="Upper Band", line=dict(color='orange', dash='dash')))
            fig_bollinger.add_trace(go.Scatter(x=df['Date'], y=df['lower_band'], mode='lines', name="Lower Band", line=dict(color='orange', dash='dash')))
            fig_bollinger.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig_bollinger, use_container_width=True)

            # Keltner Channel
            st.subheader("Keltner Channel")
            df['ema'] = df['Close'].ewm(span=20).mean()  # Exponential Moving Average (EMA)
            df['true_range'] = np.maximum(df['High'] - df['Low'], np.maximum(abs(df['High'] - df['Close'].shift(1)), abs(df['Low'] - df['Close'].shift(1))))  # True Range
            df['average_true_range'] = df['true_range'].rolling(window=20).mean()  # Average True Range (ATR)
            df['upper_keltner'] = df['ema'] + 2 * df['average_true_range']  # Upper Keltner Channel
            df['lower_keltner'] = df['ema'] - 2 * df['average_true_range']  # Lower Keltner Channel
            st.write("""
            **Keltner Channels** are volatility-based envelopes around a central moving average. The upper and lower bands are created using the Exponential Moving Average (EMA) and the Average True Range (ATR). These channels are used to identify potential buy or sell signals based on price behavior within the channels.
            """)
            fig_keltner = go.Figure()
            fig_keltner.add_trace(go.Scatter(x=df['Date'], y=df['ema'], mode='lines', name="EMA", line=dict(color='purple')))
            fig_keltner.add_trace(go.Scatter(x=df['Date'], y=df['upper_keltner'], mode='lines', name="Upper Keltner", line=dict(color='orange', dash='dash')))
            fig_keltner.add_trace(go.Scatter(x=df['Date'], y=df['lower_keltner'], mode='lines', name="Lower Keltner", line=dict(color='orange', dash='dash')))
            fig_keltner.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig_keltner, use_container_width=True)

            # Donchian Channels
            st.subheader("Donchian Channels")
            df['donchian_upper'] = df['High'].rolling(window=20).max()  # Upper Donchian Channel
            df['donchian_lower'] = df['Low'].rolling(window=20).min()  # Lower Donchian Channel
            st.write("""
            **Donchian Channels** show the highest high and the lowest low over a set period, typically 20 periods. They are useful for identifying breakouts and volatility in the market. The upper and lower channels represent key levels of support and resistance.
            """)
            fig_donchian = go.Figure()
            fig_donchian.add_trace(go.Scatter(x=df['Date'], y=df['donchian_upper'], mode='lines', name="Upper Donchian", line=dict(color='purple', dash='dash')))
            fig_donchian.add_trace(go.Scatter(x=df['Date'], y=df['donchian_lower'], mode='lines', name="Lower Donchian", line=dict(color='orange', dash='dash')))
            fig_donchian.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig_donchian, use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching data: {e}")

elif subpage == "Trade & Market Behavior Analysis":
    st.title("📈 Trade & Market Behavior Analysis")
    st.write("""
    - **Number of Trades Over Time (Trades Analysis)**
    - **Cumulative Return Plot**
    - **Relative Performance Comparison**
    - **Elder’s Force Index (EFI)** (Trend Strength)
    """)

    # Sidebar Inputs for Stock Symbol and Date Range
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

    # Fetch Stock Data
    if stock_symbol:
        try:
            stock = yf.Ticker(stock_symbol)
            df = stock.history(start=start_date, end=end_date)
            df.reset_index(inplace=True)

            # Number of Trades Over Time
            st.subheader("Number of Trades Over Time")
            df['Trades'] = df['Volume'] 
            st.write("""
            This indicator shows how the number of trades has evolved over time. 
            It's used to analyze trading activity and identify periods of high or low market participation. 
            For this, you would typically look for trade signals such as buy and sell points, and then plot the count of trades over time.
            """)  
            fig_trades = go.Figure()
            fig_trades.add_trace(go.Scatter(x=df['Date'], y=df['Trades'], mode='lines', name="Number of Trades", line=dict(color='white')))
            fig_trades.update_layout(xaxis_title="Date", yaxis_title="Number of Trades")
            st.plotly_chart(fig_trades, use_container_width=True)

            # Cumulative Return Plot
            st.subheader("Cumulative Return Plot")
            df['Daily Return'] = df['Close'].pct_change()
            df['Cumulative Return'] = (1 + df['Daily Return']).cumprod() - 1
            st.write("""
            This shows the cumulative return of an investment over time, which is calculated by compounding the percentage returns each day.
            """)
            fig_cumulative_return = go.Figure()
            fig_cumulative_return.add_trace(go.Scatter(x=df['Date'], y=df['Cumulative Return'], mode='lines', name="Cumulative Return", line=dict(color='white')))
            fig_cumulative_return.update_layout(xaxis_title="Date", yaxis_title="Cumulative Return")
            st.plotly_chart(fig_cumulative_return, use_container_width=True)

            # Relative Performance Comparison
            st.subheader("Relative Performance Comparison")
            benchmark_data = df['Close'].pct_change().cumsum()  # Cumulative return of the benchmark
            st.write("""This compares the performance of a stock relative to a benchmark (e.g., S&P 500). 
            It helps to identify whether the stock is outperforming or underperforming the benchmark.
            """)
            fig_relative_performance = go.Figure()
            fig_relative_performance.add_trace(go.Scatter(x=df['Date'], y=df['Cumulative Return'], mode='lines', name="Asset Performance", line=dict(color='grey')))
            fig_relative_performance.add_trace(go.Scatter(x=df['Date'], y=benchmark_data, mode='lines', name="Benchmark", line=dict(color='white')))
            fig_relative_performance.update_layout(xaxis_title="Date", yaxis_title="Cumulative Return")
            st.plotly_chart(fig_relative_performance, use_container_width=True)

            # Elder’s Force Index (EFI) (Trend Strength)
            st.subheader("Elder’s Force Index (EFI) (Trend Strength)")
            df['EFI'] = df['Volume'] * (df['Close'] - df['Close'].shift(1))
            st.write("""The **Elder's Force Index (EFI)** is used to measure the strength of a trend by combining price and volume. 
                     It can help identify whether a trend is strong enough to continue or likely to reverse.""")
            fig_efi = go.Figure()
            fig_efi.add_trace(go.Scatter(x=df['Date'], y=df['EFI'], mode='lines', name="EFI", line=dict(color='white')))
            fig_efi.update_layout(xaxis_title="Date", yaxis_title="EFI")
            st.plotly_chart(fig_efi, use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching data: {e}")