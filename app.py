import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.markdown(
    """
    <h1 style='display: flex; align-items: center; gap: 10px;'>
        <span>🔥 Rising Meme Coins (via DexScreener)</span>
    </h1>
    """,
    unsafe_allow_html=True
)

def fetch_dexscreener_trending(chain):
    url = f"https://api.dexscreener.com/latest/dex/tokens/trending?chain={chain}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if "pairs" not in data:
            st.warning(f"No trending data for {chain}")
            return []
        table = []
        for pair in data["pairs"]:
            price_change = pair.get("priceChange", "N/A")
            vol_24h = pair.get("volume", {}).get("h24", "N/A")
            table.append({
                "Name": pair.get("baseToken", {}).get("symbol", "N/A") + " / " + pair.get("quoteToken", {}).get("symbol", "N/A"),
                "Price (USD)": pair.get("priceUsd", "N/A"),
                "24h Vol (USD)": vol_24h,
                "Price Change 24h (%)": price_change,
                "Pair Link": f"[View]({pair.get('url', '')})"
            })
        # Sort by highest price gain in 24h (descending)
        table = sorted(table, key=lambda x: float(x["Price Change 24h (%)"].replace('%', '').replace('N/A', '-999')) if x["Price Change 24h (%)"] not in ["N/A", None] else -999, reverse=True)
        return table
    except Exception as e:
        st.error(f"Failed to fetch {chain} data: {e}")
        return []

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 Ethereum (DEX Screener)")
    eth_data = fetch_dexscreener_trending("ethereum")
    if eth_data:
        st.dataframe(pd.DataFrame(eth_data))
    else:
        st.info("No trending meme coins found for Ethereum.")

with col2:
    st.markdown("### 🛸 Base (DEX Screener)")
    base_data = fetch_dexscreener_trending("base")
    if base_data:
        st.dataframe(pd.DataFrame(base_data))
    else:
        st.info("No trending meme coins found for Base.")
