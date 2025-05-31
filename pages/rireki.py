import streamlit as st
import datetime

st.title("履歴")

d = st.date_input('見たい日付を選択してください', datetime.date(2025, 4, 1))
st.write(d)
