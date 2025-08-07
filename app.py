import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="🦎 Gecko Meme Tracker", layout="wide")
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
            try:
                attr = item["attributes"]
                token = attr["tokens"]["base"]
                trending.append({
                    "Token": token["name"],
                    "Symbol": token["symbol"],
                    "Price ($)": float(token.get("price_usd", 0.0)),
                    "24h Volume ($)": float(attr.get("volume_usd", {}).get("h24", 0)),
                    "Liquidity ($)": float(attr.get("reserve_in_usd", 0)),
                    "DEX": attr.get("dex_name", ""),
                    "Pair Link": f'https://www.geckoterminal.com/eth/pools/{item["id"].split("/")[-1]}'
                })
            except Exception as inner_err:
                continue

        trending_sorted = sorted(trending, key=lambda x: x["24h Volume ($)"], reverse=True)
        return trending_sorted[:10]

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

with st.spinner("Loading data..."):
    coins = fetch_gecko_data()

if coins:
    df = pd.DataFrame(coins)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data found.")
