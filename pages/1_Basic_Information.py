import streamlit as st
import yfinance as yf
import pandas as pd

# Set page title
st.set_page_config(page_title="Quantum Quotient Analytics", layout="wide")

st.title("Quantum Quotient Analytics")
    
# Sidebar - Stock Symbol Input and Date Selection
with st.sidebar.expander("Basic Information", expanded=True):
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "AAPL")
    start_date = st.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("today"))
    
# Fetch stock data
if stock_symbol:
    try:
        stock = yf.Ticker(stock_symbol)
        df = stock.history(start=start_date, end=end_date)
        df.reset_index(inplace=True)
        df.insert(0, "Serial No.", range(1, len(df) + 1))  # Adding Serial No.
        df = df[["Serial No.", "Date", "Open", "High", "Low", "Close", "Volume"]]  # Selected columns
            
        # Display stock data table
        st.subheader(f"Stock Data Table for {stock_symbol.upper()}")
        st.dataframe(df, width=1000)
            
        # Additional Company Information
        st.subheader("Company Information")
        info = stock.info  # Get stock metadata
        company_name = info.get("longName", "N/A")
        industry = info.get("industry", "N/A")
        exchange = info.get("exchange", "N/A")
        website = info.get("website", "N/A")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        eps = info.get("trailingEps", "N/A")
            
        # Display company details
        st.markdown(f"**Company Name:** {company_name}")
        st.markdown(f"**Industry:** {industry}")
        st.markdown(f"**Exchange:** {exchange}")
        st.markdown(f"**Website:** [Visit Website]({website})" if website != "N/A" else "**Website:** N/A")
        st.markdown(f"**Market Cap:** {market_cap}")
        st.markdown(f"**P/E Ratio:** {pe_ratio}")
        st.markdown(f"**Earnings Per Share (EPS):** {eps}")
        
    except Exception as e:
        st.error(f"Error fetching data for {stock_symbol.upper()}. Please check the symbol and try again.")