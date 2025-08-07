import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="🦎 Gecko Meme Tracker", layout="wide")
st.title("🦎 Trending Meme Coins (via GeckoTerminal)")

@st.cache_data(ttl=60)
def fetch_gecko_data():
    networks = ["eth", "base"]
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    all_data = []

    for net in networks:
        url = f"https://api.geckoterminal.com/api/v2/networks/{net}/pools/trending"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            json_data = response.json()["data"]

            for item in json_data:
                attr = item.get("attributes", {})
                token_info = attr.get("base_token", {})
                all_data.append({
                    "Token": token_info.get("name", "N/A"),
                    "Symbol": token_info.get("symbol", "N/A"),
                    "Price ($)": float(attr.get("price_usd", 0)),
                    "Volume (24h)": float(attr.get("volume_usd", 0)),
                    "Liquidity ($)": float(attr.get("liquidity_usd", 0)),
                    "DEX": attr.get("dex_name", "N/A"),
                    "Network": net,
                    "Link": f'https://www.geckoterminal.com/{net}/pools/{item.get("id", "").split("_")[-1]}'
                })

        except Exception as e:
            st.error(f"API Error for {net.upper()}: {e}")

    return all_data


with st.spinner("Fetching trending data from GeckoTerminal..."):
    data = fetch_gecko_data()

if data:
    st.dataframe(pd.DataFrame(data), use_container_width=True)
else:
    st.warning("No data found.")
