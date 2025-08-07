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

def get_rising_memes(chain):
    # DexScreener search with 'meme' for broad catch of meme tokens
    url = f"https://api.dexscreener.com/latest/dex/search/?q=meme"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if "pairs" not in data:
            st.warning(f"No meme pairs found in API response")
            return []
        # Only keep pairs on the right chain
        meme_pairs = [
            p for p in data["pairs"]
            if p.get("chainId", "").lower() == chain.lower()
        ]
        # Calculate 24h % change (some may be None or missing)
        for p in meme_pairs:
            try:
                p["priceChangePct"] = float(p.get("priceChange", "0").replace('%', ''))
            except Exception:
                p["priceChangePct"] = -9999
        # Sort by biggest 24h price gain
        meme_pairs = sorted(meme_pairs, key=lambda x: x["priceChangePct"], reverse=True)
        table = []
        for pair in meme_pairs[:25]:  # top 25 risers
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
        st.error(f"Failed to fetch meme coins for {chain}: {e}")
        return []

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 Ethereum Rising Meme Coins")
    eth_data = get_rising_memes("ethereum")
    if eth_data:
        st.dataframe(pd.DataFrame(eth_data))
    else:
        st.info("No rising meme coins found for Ethereum.")

with col2:
    st.markdown("### 🛸 Base Rising Meme Coins")
    base_data = get_rising_memes("base")
    if base_data:
        st.dataframe(pd.DataFrame(base_data))
    else:
        st.info("No rising meme coins found for Base.")
