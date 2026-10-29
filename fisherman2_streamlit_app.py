import random
import time

import streamlit as st

# ---------- ثابت‌ها ----------
LB_TO_KG = 0.45359237      # ۱ پوند به کیلوگرم
PRICE_PER_KG = 2           # دلار به ازای هر کیلوگرم
BONUS_LIMIT = 100          # حد دریافت جایزه (دلار)
PRIZES = ["🧢 کلاه", "🪝 قلاب", "🪣 سطل"]

st.set_page_config(page_title="ماهیگیر", page_icon="🎣", layout="centered")

st.title("🎣 ماهیگیر")
st.caption("وزن صیدت را به پوند بنویس تا مبلغ و جایزه‌ات را حساب کنیم.")

# ---------- ورودی ----------
with st.container(border=True):
    pounds = st.number_input(
        "چند پوند ماهی گرفته‌ای؟", min_value=0.0, value=80.0, step=1.0, format="%.2f"
    )
    pounds = st.slider("یا با نوار تنظیم کن", 0.0, 300.0, float(pounds), step=1.0)
    clicked = st.button("💰 حساب کن", type="primary", use_container_width=True)

if clicked:
    if pounds <= 0:
        st.error("یک وزن بیشتر از صفر وارد کن.")
        st.session_state.pop("res", None)
    else:
        kg = pounds * LB_TO_KG                    # تبدیل پوند به کیلوگرم
        total = kg * PRICE_PER_KG                 # محاسبه مبلغ
        won = total > BONUS_LIMIT                 # بیشتر از ۱۰۰ دلار؟
        st.session_state["res"] = {
            "pounds": pounds,
            "kg": kg,
            "total": total,
            "won": won,
            "winner": random.choice(PRIZES) if won else None,   # انتخاب تصادفی جایزه
            "spin": won,                          # انیمیشن فقط یک بار
        }

# ---------- خروجی ----------
res = st.session_state.get("res")
if res:
    st.divider()

    c1, c2, c3 = st.columns(3)
    c1.metric("وزن (پوند)", f"{res['pounds']:,.2f}")
    c2.metric("وزن (کیلوگرم)", f"{res['kg']:,.2f}")
    c3.metric("مبلغ دریافتی", f"${res['total']:,.2f}")

    st.progress(min(res["total"] / BONUS_LIMIT, 1.0), text=f"مسیر رسیدن به جایزه ({BONUS_LIMIT} دلار)")

    if res["won"]:
        st.success("مبلغت بیشتر از ۱۰۰ دلار شد. جایزه داری!", icon="🏆")
        slot = st.empty()

        if res["spin"]:
            # چرخش بین جایزه‌ها تا روی برنده بایستد
            for i in range(12 + PRIZES.index(res["winner"])):
                slot.header(PRIZES[i % len(PRIZES)])
                time.sleep(0.08 + i * 0.015)
            res["spin"] = False
            st.balloons()

        slot.header(f"🎁 {res['winner']}")
    else:
        need_lb = (BONUS_LIMIT / PRICE_PER_KG) / LB_TO_KG
        st.info(f"برای جایزه باید بیشتر از {need_lb:.1f} پوند ماهی بگیری.", icon="🎣")