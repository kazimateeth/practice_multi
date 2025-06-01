import streamlit as st
import datetime

if "username" not in st.session_state:
    st.write("履歴を利用するには評価ページにてログインしてください")
elif "username" in st.session_state:
    st.title("履歴")
    d = st.date_input('見たい日付を選択してください', datetime.date(2025, 4, 1))
    st.write(d)
    st.sidebar.success(f"{st.session_state.username} さんとしてログイン中")
    if st.sidebar.button("ログアウト"):
        del st.session_state.username
        st.rerun()