import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Predictive Modeling", layout="wide")

# Function to fetch stock data
def load_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data

st.title("🫧 Stock Predictive Modeling")
# Sidebar Inputs for Stock Symbol and Date Range
st.sidebar.header("Stock Predictive Modeling")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, MSFT, GOOGL)", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Fetch Stock Data
if stock_symbol:
    try:
        df = load_data(stock_symbol, start_date, end_date)
        # Feature Engineering: Add features like previous day's close and moving averages
        df['Prev Close'] = df['Close'].shift(1)  # Previous day's closing price
        df['MA50'] = df['Close'].rolling(window=50).mean()  # 50-day Moving Average
        df['MA200'] = df['Close'].rolling(window=200).mean()  # 200-day Moving Average
        df.dropna(inplace=True)  # Drop rows with NaN values

        # Sidebar options for selecting features
        selected_features = st.sidebar.multiselect("Select features:", ['Prev Close', 'MA50', 'MA200', 'Open', 'High', 'Low', 'Adj Close'])

        # Split data into features and target
        X = df[selected_features]
        y = df['Close']  # Target: Closing Price

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model training
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Prediction
        def predict_close_price(features):
            return model.predict([features])[0]

        # Get user input for feature values
        user_input_features = {}
        for feature in selected_features:
            user_input_features[feature] = st.sidebar.number_input(f"Enter value for {feature}:", value=0.0)

        # Predict close price   
        predicted_close = predict_close_price([user_input_features[feature] for feature in selected_features])

        # Display predicted close price
        st.subheader("Predicted Close Price")
        st.write(f"The predicted close price is: ${predicted_close:.2f}")

        # Model evaluation
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Display model metrics
        st.subheader("Model Metrics")
        st.write(f"Mean Squared Error: {mse:.2f}")
        st.write(f"R-squared Score: {r2:.2f}")

        # Plot actual vs predicted values (Interactive)
        st.subheader("Actual vs Predicted Closing Prices")
        fig_actual_predicted = go.Figure()

        # Plot Actual values
        fig_actual_predicted.add_trace(go.Scatter(
            x=df['Date'].iloc[-len(y_test):],
            y=y_test,
            mode='lines',
            name='Actual',
            line=dict(color='darkcyan')
        ))

        # Plot Predicted values
        fig_actual_predicted.add_trace(go.Scatter(
            x=df['Date'].iloc[-len(y_pred):],
            y=y_pred,
            mode='lines',
            name='Predicted',
            line=dict(color='crimson', dash='dash')
        ))

        fig_actual_predicted.update_layout(
            xaxis_title="Date",
            yaxis_title="Closing Price (USD)",
            hovermode='closest'
        )

        st.plotly_chart(fig_actual_predicted, use_container_width=True)

        # Residuals Plot (Interactive)
        st.subheader("Residuals Plot")
        residuals = y_test - y_pred
        fig_residuals = go.Figure()

        # Plot Residuals
        fig_residuals.add_trace(go.Scatter(
            x=y_pred,
            y=residuals,
            mode='markers',
            name='Residuals',
            marker=dict(color='crimson', size=8)
        ))

        # Horizontal line at 0 (Residuals = 0)
        fig_residuals.add_trace(go.Scatter(
            x=[min(y_pred), max(y_pred)],
            y=[0, 0],
            mode='lines',
            name='Residuals = 0',
            line=dict(color='darkcyan', dash='dash')
        ))

        fig_residuals.update_layout(
            xaxis_title="Predicted Values",
            yaxis_title="Residuals",
            hovermode='closest'
        )

        st.plotly_chart(fig_residuals, use_container_width=True)

    except Exception as e:
        st.write(f"Could not fetch or process data for {stock_symbol}: {e}")