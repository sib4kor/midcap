import yfinance as yf
import pandas as pd
import streamlit as st

# Top 5 MIDCAP SELECT stocks
stocks = {
    "UNIONBANK.NS": 6.12,
    "CUMMINSIND.NS": 5.69,
    "MUTHOOTFIN.NS": 5.63,
    "INDUSTOWER.NS": 5.13,
    "BSE.NS": 5.12
}

st.title("MIDCPNIFTY Live Trading Dashboard")

data = []
total_score = 0

for symbol, weight in stocks.items():
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d", interval="5m")

    if len(hist) > 1:
        open_price = hist['Open'][0]
        current_price = hist['Close'][-1]
        change_pct = ((current_price - open_price) / open_price) * 100
        
        weighted_score = change_pct * weight
        total_score += weighted_score

        data.append({
            "Stock": symbol,
            "Price": round(current_price, 2),
            "% Change": round(change_pct, 2),
            "Weight": weight,
            "Impact": round(weighted_score, 2)
        })

df = pd.DataFrame(data)

# Display table
st.dataframe(df)

# Decision Logic
st.subheader("Market Signal")

if total_score > 20:
    st.success("🔥 STRONG BULLISH - Buy CE")
elif total_score > 5:
    st.info("📈 Mild Bullish")
elif total_score < -20:
    st.error("🔻 STRONG BEARISH - Buy PE")
elif total_score < -5:
    st.warning("📉 Mild Bearish")
else:
    st.write("⚖️ Sideways Market")

st.write(f"Total Strength Score: {round(total_score,2)}")
