import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(layout="wide")
st.markdown(
    """
    <h1 style='display: flex; align-items: center; gap: 10px;'>
        <img src='https://raw.githubusercontent.com/geckoterminal/geckoterminal-branding/main/logo/logo.svg' width='30'/>
        Trending Meme Coins (via GeckoTerminal)
    </h1>
    """,
    unsafe_allow_html=True
)

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

def fetch_gecko_data(network: str, delay_between_calls: float = 2.5):
    base_url = f"https://api.geckoterminal.com/api/v2/networks/{network}/trending_pools"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        pools = response.json()["data"]
    except Exception as e:
        st.error(f"API Error for {network.upper()}: {e}")
        return []

    pool_data = []
    for item in pools:
        full_id = item["id"]  # e.g., "eth_0xabc123..."
        parts = full_id.split("_")
        if len(parts) != 2:
            st.warning(f"Unexpected pool ID format: {full_id}")
            continue

        network_prefix = parts[0]
        pool_id = parts[1]
        pool_url = f"https://api.geckoterminal.com/api/v2/networks/{network_prefix}/pools/{pool_id}"

        try:
            pool_response = requests.get(pool_url, headers=headers)
            if pool_response.status_code == 429:
                st.warning(f"Rate limit hit while fetching pool {pool_id}, skipping.")
                continue
            pool_response.raise_for_status()
            pool_info = pool_response.json()["data"]["attributes"]

            pool_data.append({
                "Pool": pool_info.get("name", "N/A"),
                "Base Token": pool_info.get("base_token", {}).get("name", "N/A"),
                "Quote Token": pool_info.get("quote_token", {}).get("name", "N/A"),
                "Price (USD)": safe_float(pool_info.get("price_usd", "N/A")),
                "Volume (24h)": safe_dollar(pool_info.get("volume_usd", "N/A")),
                "Tx Count (24h)": pool_info.get("tx_count_24h", "N/A"),
                "Link": f"[View](https://www.geckoterminal.com/{network_prefix}/pools/{pool_id})"
            })

        except Exception as e:
            st.warning(f"Pool fetch error for {full_id}: {e}")

        time.sleep(delay_between_calls)

    return pool_data

# Fetch and display Ethereum and Base separately
eth_data = fetch_gecko_data("eth", delay_between_calls=2.5)
base_data = fetch_gecko_data("base", delay_between_calls=2.5)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 Ethereum Trending Pools")
    if eth_data:
        st.dataframe(pd.DataFrame(eth_data))
    else:
        st.info("No Ethereum trending data found.")

with col2:
    st.markdown("### 🛸 Base Trending Pools")
    if base_data:
        st.dataframe(pd.DataFrame(base_data))
    else:
        st.info("No Base trending data found.")
