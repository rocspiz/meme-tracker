import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Trending Meme Coins", layout="wide")

st.markdown(
    "<h1 style='display: flex; align-items: center;'>🦎 Trending Meme Coins (via GeckoTerminal)</h1>",
    unsafe_allow_html=True
)

def fetch_gecko_data(network):
    url = f"https://api.geckoterminal.com/api/v2/networks/{network}/trending_pools"
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
            url_slug = item.get("id", "")
            pool_url = f"https://www.geckoterminal.com/{network}/pools/{url_slug}"

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

# --- Fetch data ---
eth_data = fetch_gecko_data("eth")
base_data = fetch_gecko_data("base")

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 Ethereum Trending Pools")
    if eth_data:
        eth_df = pd.DataFrame(eth_data)
        st.dataframe(eth_df, use_container_width=True)
    else:
        st.info("No Ethereum trending data found.")

with col2:
    st.markdown("### 🛸 Base Trending Pools")
    if base_data:
        base_df = pd.DataFrame(base_data)
        st.dataframe(base_df, use_container_width=True)
    else:
        st.info("No Base trending data found.")
