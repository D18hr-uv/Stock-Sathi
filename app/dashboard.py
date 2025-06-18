import streamlit as st
import pandas as pd
from scripts.fetch_data import fetch_stock_data
from scripts.plot_graphs import plot_stock_price
from scripts.alert import check_price_alert

st.set_page_config(page_title="📈 Stock Dashboard", layout="wide")
st.title("📈 Real-Time Stock Analysis Dashboard")

# Sidebar controls
symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
interval = st.sidebar.selectbox("Select Interval", ["1m", "5m", "15m", "1h", "1d"], index=0)
period = st.sidebar.selectbox("Select Period", ["1d", "5d", "1mo", "3mo"], index=0)
threshold = st.sidebar.slider("Set Alert Threshold (%)", 1, 10, 5)

# Fetch data
if symbol:
    data = fetch_stock_data(symbol, interval, period)
    if not data.empty:
        st.subheader(f"📊 {symbol} - Last Price: {data['Close'].iloc[-1]:.2f}")
        st.dataframe(data.tail(), height=200)

        # Plot chart
        fig = plot_stock_price(data, f"{symbol} Price Over Time")
        st.plotly_chart(fig, use_container_width=True)

        # Alert
        alert_msg = check_price_alert(data, threshold)
        st.info(alert_msg)

        # Download
        csv = data.to_csv(index=False).encode()
        st.download_button("Download CSV", data=csv, file_name=f"{symbol}_data.csv")
    else:
        st.warning("⚠️ No data found!")

