import streamlit as st
from datetime import date

today = date.today()

jacket = "上着"
tops = "トップス"
bottoms = "ボトムス"
winter_clothes = "防寒具"

evaluate = {}
evaluate["日付"] = today

st.title(today.strftime("%Y-%m-%d")+"の評価をする")

option1=["なし","ダウンジャケット","厚手の上着","薄手の上着"]
evaluate[jacket] = st.selectbox(jacket,option1)

option2=["厚めの長袖","薄手の長袖","半袖",]
evaluate[tops] = st.selectbox(tops,option2)

option3=["厚手のボトムス","薄手のボトムス","短いボトムス",]
evaluate[bottoms] = st.selectbox(bottoms,option3)

option4=["なし","しっかり","少し",]
evaluate[winter_clothes] = st.selectbox(winter_clothes,option4)

st.write("気温")
evaluate["評価"] = st.radio("これを…", ("暑かった", "寒かった", "ちょうどいい"))

#戻り値の確認用
if st.button("決定"):
    st.subheader("フィードバックを受け付けました！")
    for category, choice in evaluate.items():
        st.write(f"・{category}：{choice}")
