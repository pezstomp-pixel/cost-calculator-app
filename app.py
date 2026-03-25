import streamlit as st

st.set_page_config(page_title="展示会仕入れ計算", page_icon="🧮", layout="wide")

# 文字と余白を少し詰めるCSS
st.markdown("""
<style>
    .small-input label {font-size:14px;}
    .small-input input {font-size:16px;}
    .block-container {padding-top:0.5rem; padding-bottom:0.5rem;}
</style>
""", unsafe_allow_html=True)

st.title("展示会 仕入れ計算")

RATE_CNY = 22
RATE_USD = 150

tab1, tab2 = st.tabs(["利益計算", "仕入れ上限"])

# ---------- タブ1：利益計算 ----------
with tab1:
    st.subheader("利益計算")

    with st.container():
        st.markdown('<div class="small-input">', unsafe_allow_html=True)
        sell_price = st.number_input("予定販売価格 (円)", min_value=0, value=3000, step=100)
        shipping = st.number_input("送料 (円)", min_value=0, value=500, step=50)

        buy_currency = st.radio("仕入れ通貨", ["JPY", "CNY", "USD"], horizontal=True)
        buy_price_input = st.number_input(f"仕入れ値 ({buy_currency})", min_value=0.0, value=50.0, step=1.0)

        fee_rate = st.selectbox("販売手数料率", ["8%", "10%", "15%"], index=1)
        st.markdown('</div>', unsafe_allow_html=True)

    if buy_currency == "JPY":
        buy_price_jpy = buy_price_input
    elif buy_currency == "CNY":
        buy_price_jpy = buy_price_input * RATE_CNY
    else:
        buy_price_jpy = buy_price_input * RATE_USD

    fee = float(fee_rate.replace("%", "")) / 100.0

    net_sales = sell_price * (1 - fee) - shipping
    profit = net_sales - buy_price_jpy
    profit_margin = (profit / sell_price * 100) if sell_price > 0 else 0

    st.markdown("---")
    st.write(f"仕入れ原価(JPY): **{buy_price_jpy:,.0f} 円**")
    st.write(f"利益額: **{profit:,.0f} 円**")
    st.write(f"利益率: **{profit_margin:,.1f} %**")

# ---------- タブ2：仕入れ上限 ----------
with tab2:
    st.subheader("仕入れ上限")

    with st.container():
        st.markdown('<div class="small-input">', unsafe_allow_html=True)
        sell_price2 = st.number_input("予定販売価格 (円)", min_value=0, value=3000, step=100, key="sell2")
        shipping2 = st.number_input("送料 (円)", min_value=0, value=500, step=50, key="ship2")
        target_margin_percent = st.number_input("目標利益率 (%)", min_value=0.0, value=20.0, step=1.0)
        fee_rate2 = st.selectbox("販売手数料率", ["8%", "10%", "15%"], index=1, key="fee2")
        st.markdown('</div>', unsafe_allow_html=True)

    fee2 = float(fee_rate2.replace("%", "")) / 100.0
    target_margin = target_margin_percent / 100.0

    max_buy_price = sell_price2 * (1 - fee2 - target_margin) - shipping2

    st.markdown("---")
    if max_buy_price < 0:
        st.error(f"計算上の仕入れ上限額がマイナスです: {max_buy_price:,.0f} 円")
    else:
        st.write(f"仕入れ上限額(JPY): **{max_buy_price:,.0f} 円**")

    st.caption("レート: 1 CNY=22円, 1 USD=150円（固定）")
