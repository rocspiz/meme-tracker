import streamlit as st
import requests
import pandas as pd

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

def fetch_trending_pools(network: str):
    url = f"https://api.geckoterminal.com/api/v2/networks/{network}/trending_pools"
    headers = {"accept": "application/json"}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        pools = resp.json()["data"]
    except Exception as e:
        st.error(f"API Error for {network.upper()}: {e}")
        return []

    table = []
    for item in pools:
        attr = item.get("attributes", {})
        pool_id = item.get("id", "").split("_")[-1]
        table.append({
            "Pool": attr.get("name", "N/A"),
            "Base Token": attr.get("base_token", {}).get("name", "N/A"),
            "Quote Token": attr.get("quote_token", {}).get("name", "N/A"),
            "Price (USD)": safe_float(attr.get("price_usd")),
            "Volume (24h)": safe_dollar(attr.get("volume_usd")),
            "Tx Count (24h)": attr.get("tx_count_24h", "N/A"),
            "Link": f"[View](https://www.geckoterminal.com/{network}/pools/{pool_id})"
        })
    return table

eth_data = fetch_trending_pools("eth")
base_data = fetch_trending_pools("base")

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
