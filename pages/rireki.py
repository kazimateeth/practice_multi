import streamlit as st
import datetime
import json

with open("/Users/kazamadaishi/local/prr/practice_multi/user_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)


if "username" not in st.session_state:
    st.write("履歴を利用するには評価ページにてログインしてください")
elif "username" in st.session_state:
    st.title("履歴")
    d = st.date_input('見たい日付を選択してください', datetime.date(2025, 4, 1))
    evaluations = data.get(st.session_state.username).get(str(d))
    if evaluations is None:
       st.write(str(d)+"データは存在しません")
    else:
       for category, value in evaluations.items():
            st.write(f"・{category}: {value}")
    st.sidebar.success(f"{st.session_state.username} さんとしてログイン中")
    if st.sidebar.button("ログアウト"):
        del st.session_state.username
        st.rerun()