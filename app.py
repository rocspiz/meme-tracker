import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Meme Coin Mega Tracker", layout="wide")
st.title("🚀 Meme Coin Mega Tracker (ETH & Base)")

@st.cache_data(ttl=60)
def get_dextools_top_pairs():
    url = "https://api.dexscreener.com/latest/dex/pairs"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        pairs = response.json().get("pairs", [])
        
        filtered = [
            p for p in pairs 
            if p["chainId"] in ["eth", "base"] and p["liquidity"]["usd"] > 10000
        ]

        sorted_pairs = sorted(filtered, key=lambda x: x["volume"]["h24"], reverse=True)

        return [
            {
                "Token": p["baseToken"]["name"],
                "Symbol": p["baseToken"]["symbol"],
                "Price ($)": round(float(p["priceUsd"]), 8),
                "Market Cap ($)": int(p["fdv"]) if p["fdv"] else None,
                "Liquidity ($)": int(p["liquidity"]["usd"]),
                "24h Volume ($)": int(p["volume"]["h24"]),
                "Buys/Sells": f'{p["txns"]["buys"]}/{p["txns"]["sells"]}',
                "DEX": p["dexId"],
                "View Pair": p["url"]
            }
            for p in sorted_pairs
        ][:10]
    except Exception as e:
        st.error(f"API Error: {e}")
        return []

# Fetch and display
with st.spinner("Loading trending meme pairs..."):
    data = get_dextools_top_pairs()

if data:
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No trending pairs available or blocked API.")
