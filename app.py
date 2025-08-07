import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Trending Meme Coins", layout="wide")

st.markdown("# 🦎 Trending Meme Coins (via GeckoTerminal)")

def safe_float(val):
    try:
        return round(float(val), 6)
    except:
        return "N/A"

def safe_dollar(val):
    try:
        return f"${float(val):,.0f}"
    except:
        return "N/A"

def fetch_gecko_data(network):
    trending_url = f"https://api.geckoterminal.com/api/v2/networks/{network}/trending_pools"
    try:
        response = requests.get(trending_url)
        response.raise_for_status()
        trending = response.json().get("data", [])
        detailed_data = []

        for item in trending:
            pool_id = item["id"]
            pool_url = f"https://api.geckoterminal.com/api/v2/networks/{network}/pools/{pool_id}"
            try:
                detail_resp = requests.get(pool_url)
                detail_resp.raise_for_status()
                data = detail_resp.json().get("data", {})
                attr = data.get("attributes", {})

                pool_name = attr.get("name", "Unknown")
                base_token = attr.get("base_token", {}).get("name", "N/A")
                quote_token = attr.get("quote_token", {}).get("name", "N/A")
                price_usd = safe_float(attr.get("price_usd"))
                volume_usd = safe_dollar(attr.get("volume_usd"))
                tx_count = attr.get("tx_count_24h", "N/A")
                pool_link = f"https://www.geckoterminal.com/{network}/pools/{pool_id}"

                detailed_data.append({
                    "Pool": pool_name,
                    "Base Token": base_token,
                    "Quote Token": quote_token,
                    "Price (USD)": price_usd,
                    "Volume (24h)": volume_usd,
                    "Tx Count (24h)": tx_count,
                    "Link": f"[View]({pool_link})"
                })
            except Exception as e:
                print(f"Failed fetching detail for pool {pool_id}: {e}")

        return detailed_data
    except Exception as e:
        st.error(f"API Error for {network.upper()}: {e}")
        return []

eth_data = fetch_gecko_data("eth")
base_data = fetch_gecko_data("base")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 Ethereum Trending Pools")
    if eth_data:
        df_eth = pd.DataFrame(eth_data)
        st.dataframe(df_eth, use_container_width=True)
    else:
        st.info("No Ethereum trending data found.")

with col2:
    st.markdown("### 🛸 Base Trending Pools")
    if base_data:
        df_base = pd.DataFrame(base_data)
        st.dataframe(df_base, use_container_width=True)
    else:
        st.info("No Base trending data found.")
