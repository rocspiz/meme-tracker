import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.markdown(
    "<h1>🚀 Trending Exploding Coins (via Birdeye / Solana)</h1>",
    unsafe_allow_html=True
)

def get_birdeye_trending(top_n=20):
    url = "https://public-api.birdeye.so/public/trending"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        tokens = data.get("data", [])
        # Sort by 24h gain
        for t in tokens:
            try:
                t["priceChangePct"] = float(t.get("priceChange24h", 0))
            except Exception:
                t["priceChangePct"] = -9999
        tokens = sorted(tokens, key=lambda x: x["priceChangePct"], reverse=True)
        table = []
        for token in tokens[:top_n]:
            table.append({
                "Name": token.get("tokenSymbol", "N/A"),
                "Price (USD)": token.get("priceUsd", "N/A"),
                "Volume (24h)": f"${token.get('volume24h', 0):,.0f}",
                "Price Change 24h (%)": f"{token.get('priceChange24h', 0):.2f}",
                "Pair Link": f"[View](https://birdeye.so/token/{token.get('address', '')})"
            })
        return table
    except Exception as e:
        st.error(f"Failed to fetch trending coins: {e}")
        return []

st.markdown("### 🟢 Top 20 Trending Coins: Solana (via Birdeye)")
sol_data = get_birdeye_trending(20)
if sol_data:
    st.dataframe(pd.DataFrame(sol_data))
else:
    st.info("No trending coins found for Solana.")
