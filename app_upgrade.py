import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# -----------------------------
# Top 5 MIDCAP SELECT stocks with their weights
# -----------------------------
stocks = {
    "UNIONBANK.NS": 6.12,
    "CUMMINSIND.NS": 5.69,
    "MUTHOOTFIN.NS": 5.63,
    "INDUSTOWER.NS": 5.13,
    "BSE.NS": 5.12
}

st.set_page_config(page_title="MIDCPNIFTY Dashboard", layout="wide")
st.title("MIDCPNIFTY Live Multi-Timeframe Dashboard")

# -----------------------------
# Timeframes
# -----------------------------
timeframes = {
    "5m": "5-Minute",
    "15m": "15-Minute",
    "1d": "1-Day",
    "1wk": "1-Week",
    "1mo": "1-Month"
}

# -----------------------------
# Helper function to fetch data
# -----------------------------
def fetch_data(symbol, interval):
    if interval in ["5m", "15m"]:
        hist = yf.Ticker(symbol).history(period="7d", interval=interval)
    else:
        hist = yf.Ticker(symbol).history(period="1y", interval=interval)
    return hist

# -----------------------------
# Loop over timeframes
# -----------------------------
for interval, label in timeframes.items():
    st.subheader(f"{label} Analysis")
    
    cumulative_score = 0
    fig = go.Figure()
    
    df_table = []
    
    for symbol, weight in stocks.items():
        hist = fetch_data(symbol, interval)
        if len(hist) < 2:
            continue
        
        open_price = hist['Open'][0]
        current_price = hist['Close'][-1]
        change_pct = ((current_price - open_price)/open_price)*100
        impact = change_pct * weight
        cumulative_score += impact
        
        # Add to table
        df_table.append({
            "Stock": symbol,
            "Price": round(current_price,2),
            "% Change": round(change_pct,2),
            "Weight": weight,
            "Impact": round(impact,2)
        })
        
        # Add line chart trace
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist['Close'],
            mode='lines',
            name=symbol
        ))
    
    # Display Table
    df_display = pd.DataFrame(df_table)
    st.dataframe(df_display, use_container_width=True)
    
    # Display Line Chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Display Cumulative Score & Signal
    st.markdown("**Cumulative Index Impact:** {:.2f}".format(cumulative_score))
    
    if cumulative_score > 20:
        st.success("🔥 STRONG BULLISH")
    elif cumulative_score > 5:
        st.info("📈 Mild Bullish")
    elif cumulative_score < -20:
        st.error("🔻 STRONG BEARISH")
    elif cumulative_score < -5:
        st.warning("📉 Mild Bearish")
    else:
        st.write("⚖️ Sideways Market")
    
    st.markdown("---")
