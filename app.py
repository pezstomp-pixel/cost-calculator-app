import streamlit as st

st.set_page_config(page_title="Cost Calculator", page_icon="🧮", layout="wide")

# 文字と余白を少し詰めるCSS
st.markdown("""
<style>
    .small-input label {font-size:14px;}
    .small-input input {font-size:16px;}
    .block-container {padding-top:0.5rem; padding-bottom:0.5rem;}
</style>
""", unsafe_allow_html=True)

st.title("Cost Calculator")

RATE_CNY = 22
RATE_USD = 150

tab1, tab2 = st.tabs(["利益計算", "仕入値上限額"])

# ---------- タブ1：利益計算 ----------
with tab1:
    st.subheader("利益計算")

    with st.container():
        st.markdown('<div class="small-input">', unsafe_allow_html=True)
        sell_price = st.number_input("予定販売価格 (円)", min_value=0, value=3000, step=100)
        shipping = st.number_input("送料 (円)", min_value=0, value=500, step=50)

        # ラベル変更「仕入れ通貨 → 通貨」、初期位置 CNY
        currency_options = ["JPY", "CNY", "USD"]
        buy_currency = st.radio("通貨", currency_options, index=1, horizontal=True)

        # 通貨ごとの初期値
        default_by_currency = {
            "JPY": 1500.0,
            "CNY": 68.0,
            "USD": 10.0,
        }
        buy_price_input = st.number_input(
            f"仕入れ値 ({buy_currency})",
            min_value=0.0,
            value=default_by_currency[buy_currency],
            step=1.0,
        )

        fee_rate = st.selectbox("販売手数料率", ["8%", "10%", "15%"], index=1)
        st.markdown('</div>', unsafe_allow_html=True)

    # 通貨換算
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


# ---------- タブ2：仕入値上限額 ----------
with tab2:
    st.subheader("仕入値上限額")

    with st.container():
        st.markdown('<div class="small-input">', unsafe_allow_html=True)
        sell_price2 = st.number_input("予定販売価格 (円)", min_value=0, value=3000, step=100, key="sell2")
        shipping2 = st.number_input("送料 (円)", min_value=0, value=500, step=50, key="ship2")

        # 目標利益率 初期値 40%
        target_margin_percent = st.number_input("目標利益率 (%)", min_value=0.0, value=40.0, step=1.0)
        fee_rate2 = st.selectbox("販売手数料率", ["8%", "10%", "15%"], index=1, key="fee2")
        st.markdown('</div>', unsafe_allow_html=True)

    fee2 = float(fee_rate2.replace("%", "")) / 100.0
    target_margin = target_margin_percent / 100.0

    # JPYでの仕入れ上限
    base_max_buy_jpy = sell_price2 * (1 - fee2 - target_margin) - shipping2

    st.markdown("---")

    if base_max_buy_jpy < 0:
        st.error(f"計算上の仕入値上限(JPY)がマイナスです: {base_max_buy_jpy:,.0f} 円")
    else:
        # 各通貨で3行表示
        max_jpy = base_max_buy_jpy
        max_cny = base_max_buy_jpy / RATE_CNY
        max_usd = base_max_buy_jpy / RATE_USD

        st.write("### 仕入値上限")
        st.write(f"仕入値上限(JPY): **{max_jpy:,.0f} 円**")
        st.write(f"仕入値上限(CNY): **{max_cny:,.1f} 元**")
        st.write(f"仕入値上限(USD): **{max_usd:,.2f} ドル**")

    st.caption("レート: 1 CNY=22円, 1 USD=150円（固定）")