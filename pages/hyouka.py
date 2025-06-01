import streamlit as st
from datetime import date

today = date.today()

jacket = "上着"
tops = "トップス"
bottoms = "ボトムス"
winter_clothes = "防寒具"

evaluate = {}
evaluate["日付"] = today

st.title(today.strftime("%Y-%m-%d")+"の評価")
col1 , col2 , col3 , col4, col5 = st.columns(5)
with col1:
    option1=["ダウンジャケット","厚手の上着","薄手の上着","なし"]
    evaluate[jacket] = st.selectbox(jacket,option1)
with col2:
    option2=["厚めの長袖","薄手の長袖","半袖",]
    evaluate[tops] = st.selectbox(tops,option2)
with col3:
    option3=["厚手のボトムス","薄手のボトムス","短いボトムス",]
    evaluate[bottoms] = st.selectbox(bottoms,option3)
with col4:
    option4=["しっかり","少し","なし",]
    evaluate[winter_clothes] = st.selectbox(winter_clothes,option4)
with col5:
    st.write("気温")
    evaluate["評価"] = st.radio("これを…", ("暑かった", "寒かった", "ちょうどいい"))

#戻り値の確認用
if st.button("決定"):
    st.subheader("フィードバックを受け付けました！")
    for category, choice in evaluate.items():
        st.write(f"・{category}：{choice}")
