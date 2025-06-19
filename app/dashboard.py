import streamlit as st
import pandas as pd
import sys
import os

# Add parent path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.fetch_data import fetch_stock_data
from scripts.plot_graphs import plot_stock_price
from scripts.alert import check_price_alert

# Page setup
st.set_page_config(
    page_title="📈 Stock Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- MASSIVE UI Zoom with High Contrast -------------------
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-size: 32px !important;
            color: #111 !important;
        }
        h1, h2, h3, h4 {
            font-weight: 800;
            font-size: 48px !important;
        }
        .stButton button, .stDownloadButton button {
            font-size: 28px !important;
            padding: 0.8rem 1.6rem;
            border-radius: 12px;
        }
        .stTextInput input, .stSelectbox div div div, .stSlider span {
            font-size: 28px !important;
        }
        .metric-box {
            padding: 1.4rem;
            border-radius: 14px;
            font-weight: 900;
            margin-bottom: 1rem;
            text-align: center;
        }
        .symbol-card { background-color: #d0f0f7; color: #004d40; }
        .price-card  { background-color: #dcedc8; color: #33691e; }
        .time-card   { background-color: #ffe0b2; color: #e65100; }
    </style>
""", unsafe_allow_html=True)

# ------------------- Sidebar -------------------
st.sidebar.markdown("## ⚙️ Settings")
symbol = st.sidebar.text_input("🔍 Stock Symbol", value="AAPL")
interval = st.sidebar.selectbox("🕒 Interval", ["1m", "5m", "15m", "1h", "1d"], index=0)
period = st.sidebar.selectbox("📅 Period", ["1d", "5d", "1mo", "3mo"], index=0)
threshold = st.sidebar.slider("🚨 Alert Threshold (%)", 1, 10, 5)

# ------------------- Header -------------------
st.title("📊 Real-Time Stock Analysis Dashboard")
st.markdown("Get **massively zoomed-in**, high-contrast updates on live stock prices and alerts.")

# ------------------- Fetch Data -------------------
if symbol:
    data = fetch_stock_data(symbol, interval, period)

    if not data.empty:
        last_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2] if len(data) > 1 else last_price
        price_change = last_price - prev_price
        price_change_pct = (price_change / prev_price * 100) if prev_price else 0

        # ------------------- KPI Metrics -------------------
        st.markdown("### 🔎 Summary")
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
            <div class="metric-box symbol-card">
                Symbol<br><span style='font-size:48px'>{symbol.upper()}</span>
            </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
            <div class="metric-box price-card">
                Last Price<br><span style='font-size:48px'>${last_price:.2f}</span><br>
                <span style="color:{'green' if price_change >= 0 else 'red'}; font-size:28px;">
                    {price_change:+.2f} ({price_change_pct:+.2f}%)
                </span>
            </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
            <div class="metric-box time-card">
                Interval / Period<br><span style='font-size:44px'>{interval} / {period}</span>
            </div>
        """, unsafe_allow_html=True)

        # ------------------- Data Table -------------------
        st.markdown("### 🧾 Stock Data (Latest)")
        st.dataframe(data.tail(), height=300, use_container_width=True)

        # ------------------- Price Chart -------------------
        st.markdown("### 📈 Trend Chart")
        fig = plot_stock_price(data, f"{symbol.upper()} Price")
        st.plotly_chart(fig, use_container_width=True)

        # ------------------- Alert Message -------------------
        st.markdown("### 🚨 Alert")
        alert_msg = check_price_alert(data, threshold)
        if "No alert" in alert_msg:
            st.success(alert_msg)
        else:
            st.error(alert_msg)

        # ------------------- Download CSV -------------------
        csv = data.to_csv(index=False).encode()
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"{symbol}_data.csv",
            mime="text/csv"
        )

    else:
        st.warning("⚠️ No data found for this symbol. Try another.")
