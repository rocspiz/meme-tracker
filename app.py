import streamlit as st
import requests
import pandas as pd
import time

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

def fetch_gecko_data(network, delay_between_calls=1.2):
    trending_url = f"https://api.geckoterminal.com/api/v2/networks/{network}/trending_pools"
    detailed_data = []

    try:
        trending_resp = requests.get(trending_url)
        if trending_resp.status_code == 429:
            raise Exception("Rate limit hit. Please try again later.")
        trending_resp.raise_for_status()

        trending = trending_resp.json().get("data", [])
        for item in trending:
            pool_id = item["id"]
            pool_url = f"https://api.geckoterminal.com/api/v2/networks/{network}/pools/{pool_id}"

            try:
                time.sleep(delay_between_calls)
                pool_resp = requests.get(pool_url)
                if pool_resp.status_code == 429:
                    st.warning(f"Rate limit hit while fetching pool {pool_id}, skipping.")
                    continue
                pool_resp.raise_for_status()

                data = pool_resp.json().get("data", {})
                attr = data.get("attributes", {})

                detailed_data.append({
                    "Pool": attr.get("name", "Unknown"),
                    "Base Token": attr.get("base_token", {}).get("name", "N/A"),
                    "Quote Token": attr.get("quote_token", {}).get("name", "N/A"),
                    "Price (USD)": safe_float(attr.get("price_usd")),
                    "Volume (24h)": safe_dollar(attr.get("volume_usd")),
                    "Tx Count (24h)": attr.get("tx_count_24h", "N/A"),
                    "Link": f"[View](https://www.geckoterminal.com/{network}/pools/{pool_id})"
                })

            except Exception as pool_err:
                st.warning(f"Pool fetch error for {pool_id}: {pool_err}")

        return detailed_data

    except Exception as e:
        st.error(f"API Error for {network.upper()}: {e}")
        return []

# Fetch ETH and BASE data with delays to avoid rate limit
eth_data = fetch_gecko_data("eth", delay_between_calls=1.2)
base_data = fetch_gecko_data("base", delay_between_calls=1.2)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 Ethereum Trending Pools")
    if eth_data:
        st.dataframe(pd.DataFrame(eth_data), use_container_width=True)
    else:
        st.info("No Ethereum trending data found.")

with col2:
    st.markdown("### 🛸 Base Trending Pools")
    if base_data:
        st.dataframe(pd.DataFrame(base_data), use_container_width=True)
    else:
        st.info("No Base trending data found.")
