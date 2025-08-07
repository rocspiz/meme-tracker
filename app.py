import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.markdown(
    """
    <h1 style='display: flex; align-items: center; gap: 10px;'>
        <span>🚀 Trending Exploding Coins (via DexScreener)</span>
    </h1>
    """,
    unsafe_allow_html=True
)

def get_top_trending(chain, top_n=20):
    url = f"https://api.dexscreener.com/latest/dex/trending/{chain}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        pairs = data.get("pairs", [])
        # Calculate 24h % change
        for p in pairs:
            try:
                p["priceChangePct"] = float(str(p.get("priceChange", "0")).replace('%', ''))
            except Exception:
                p["priceChangePct"] = -9999
        # Sort by biggest 24h price gain
        pairs = sorted(pairs, key=lambda x: x["priceChangePct"], reverse=True)
        table = []
        for pair in pairs[:top_n]:
            table.append({
                "Name": f"{pair.get('baseToken', {}).get('symbol', 'N/A')} / {pair.get('quoteToken', {}).get('symbol', 'N/A')}",
                "Dex": pair.get("dexId", "N/A"),
                "Price (USD)": pair.get("priceUsd", "N/A"),
                "24h Vol (USD)": pair.get("volume", {}).get("h24", "N/A"),
                "Price Change 24h (%)": pair.get("priceChange", "N/A"),
                "Pair Link": f"[View]({pair.get('url', '')})"
            })
        return table
    except Exception as e:
        st.error(f"Failed to fetch trending pairs for {chain}: {e}")
        return []

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 Top 20 Trending Coins: Ethereum")
    eth_data = get_top_trending("ethereum", top_n=20)
    if eth_data:
        st.dataframe(pd.DataFrame(eth_data))
    else:
        st.info("No trending coins found for Ethereum.")

with col2:
    st.markdown("### 🛸 Top 20 Trending Coins: Base")
    base_data = get_top_trending("base", top_n=20)
    if base_data:
        st.dataframe(pd.DataFrame(base_data))
    else:
        st.info("No trending coins found for Base.")
