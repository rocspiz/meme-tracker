import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="🦎 Gecko Meme Tracker", layout="wide")
st.title("🦎 Trending Meme Coins (via GeckoTerminal)")

@st.cache_data(ttl=60)
def fetch_gecko_data():
    url = "https://api.geckoterminal.com/api/v2/search/trending"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()["data"]["attributes"]["trending_pools"]

        trending = []
        for item in data:
            token = item.get("base_token", {})
            trending.append({
                "Token": token.get("name", "N/A"),
                "Symbol": token.get("symbol", "N/A"),
                "Price ($)": float(item.get("price_usd", 0)),
                "Volume (24h)": float(item.get("volume_usd", 0)),
                "Liquidity ($)": float(item.get("liquidity_usd", 0)),
                "DEX": item.get("dex_name", "N/A"),
                "Link": f'https://www.geckoterminal.com/{item.get("network", "eth")}/pools/{item.get("pool_address", "")}'
            })

        return trending

    except Exception as e:
        st.error(f"API Error: {e}")
        return []

with st.spinner("Fetching trending data from GeckoTerminal..."):
    data = fetch_gecko_data()

if data:
    st.dataframe(pd.DataFrame(data), use_container_width=True)
else:
    st.warning("No data found.")
