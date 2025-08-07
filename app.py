import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="🔥 Gecko Meme Coin Tracker", layout="wide")
st.title("🦎 Trending Meme Coins (via GeckoTerminal)")

@st.cache_data(ttl=60)
def fetch_gecko_data():
    url = "https://api.geckoterminal.com/api/v2/networks/eth/pools"
    params = {"page": 1}
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()["data"]
        
        trending = []
        for item in data:
            attributes = item["attributes"]
            token_info = attributes["base_token"]
            trending.append({
                "Token": token_info["name"],
                "Symbol": token_info["symbol"],
                "Price ($)": float(attributes["base_token_price_usd"]),
                "24h Volume ($)": int(attributes["volume_usd"]["h24"]),
                "Liquidity ($)": int(attributes["reserve_in_usd"]),
                "DEX": attributes["dex_name"],
                "Pair Link": f'https://www.geckoterminal.com/eth/pools/{item["id"].split("/")[-1]}'
            })

        # Sort by volume descending
        trending_sorted = sorted(trending, key=lambda x: x["24h Volume ($)"], reverse=True)
        return trending_sorted[:10]

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# Load and display
with st.spinner("Loading live meme coins..."):
    coins = fetch_gecko_data()

if coins:
    df = pd.DataFrame(coins)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data found.")
