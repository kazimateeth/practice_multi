import streamlit as st
import datetime
import json
import os

DATA_FILE = "user_data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}


if "username" not in st.session_state:
    st.write("履歴を利用するには評価ページにてログインしてください")
elif "username" in st.session_state:
    user_history = data.get(st.session_state.username, {})
    history_dates = sorted(user_history.keys())
    # 表示例：履歴あり日リストをサイドバーに表示（色つき）
    st.sidebar.markdown("### 履歴がある日")
    for d in history_dates:
        st.sidebar.markdown(f"- 🟢 {d}")
    st.title("履歴")
    d = st.date_input('見たい日付を選択してください', datetime.date(2025, 4, 1))
    evaluations = data.get(st.session_state.username).get(str(d))
    if evaluations is None:
       st.write(str(d)+"のデータは存在しません")
    else:
       for category, value in evaluations.items():
            st.write(f"・{category}: {value}")
    st.sidebar.success(f"{st.session_state.username} さんとしてログイン中")
    if st.sidebar.button("ログアウト"):
        del st.session_state.username
        st.rerun()