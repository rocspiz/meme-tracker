import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Meme Coin Mega Tracker", layout="wide")
st.markdown("## 🦎 Trending Meme Coins (via GeckoTerminal)")

# Helper function to fetch trending pools from GeckoTerminal
def fetch_gecko_data(network):
    url = f"https://api.geckoterminal.com/api/v2/networks/{network}/pools?sort=trending"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pools = data.get("data", [])
        parsed = []
        for item in pools:
            attr = item["attributes"]
            pool_name = attr.get("name", "Unknown")
            base_token = attr.get("base_token", {}).get("name", "N/A")
            quote_token = attr.get("quote_token", {}).get("name", "N/A")
            price_usd = attr.get("price_usd", "N/A")
            volume_usd = attr.get("volume_usd", "N/A")
            tx_count = attr.get("tx_count_24h", "N/A")
            url_slug = attr.get("url_slug", "")
            pool_url = f"https://www.geckoterminal.com/network/{network}/pools/{url_slug}"

            parsed.append({
                "Pool": pool_name,
                "Base Token": base_token,
                "Quote Token": quote_token,
                "Price (USD)": round(float(price_usd), 4) if price_usd else "N/A",
                "Volume (24h)": f"${float(volume_usd):,.0f}" if volume_usd else "N/A",
                "Tx Count (24h)": tx_count,
                "Link": f"[View]({pool_url})"
            })

        return parsed
    except Exception as e:
        st.error(f"API Error for {network.upper()}: {e}")
        return []

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 Ethereum Trending Pools")
    eth_data = fetch_gecko_data("eth")
    if eth_data:
        df_eth = pd.DataFrame(eth_data)
        st.dataframe(df_eth, use_container_width=True)
    else:
        st.warning("No Ethereum trending data found.")

with col2:
    st.subheader("🪐 Base Trending Pools")
    base_data = fetch_gecko_data("base")
    if base_data:
        df_base = pd.DataFrame(base_data)
        st.dataframe(df_base, use_container_width=True)
    else:
        st.warning("No Base trending data found.")
