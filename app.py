import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="🦎 Gecko Meme Tracker", layout="wide")
st.title("🦎 Trending Meme Coins (via GeckoTerminal)")

@st.cache_data(ttl=60)
def fetch_gecko_data():
    url = "https://api.geckoterminal.com/api/v2/search/trending"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()["data"]["attributes"]["trending_pools"]

        trending = []
        for item in data:
            try:
                token = item["base_token"]
                trending.append({
                    "Token": token.get("name", ""),
                    "Symbol": token.get("symbol", ""),
                    "Price ($)": float(item.get("price_usd", 0.0)),
                    "Volume (24h)": float(item.get("volume_usd", 0.0)),
                    "Liquidity ($)": float(item.get("liquidity_usd", 0.0)),
                    "DEX": item.get("dex_name", ""),
                    "Pair Link": f'https://www.geckoterminal.com/{item.get("network", "eth")}/pools/{item.get("pool_address", "")}'
                })
            except Exception:
                continue

        return trending

    except Exception as e:
        st.error(f"API Error: {e}")
        return []

with st.spinner("Loading trending coins..."):
    data = fetch_gecko_data()

if data:
    st.dataframe(pd.DataFrame(data), use_container_width=True)
else:
    st.warning("No data found.")
