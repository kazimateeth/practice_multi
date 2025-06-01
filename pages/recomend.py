import json
import os

import streamlit as st


if "username" not in st.session_state:
    st.write("履歴を利用するには評価ページにてログインしてください")

elif "username" in st.session_state:
    DATA_FILE = "user_data.json"

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            user_data = json.load(f)
    else:
        user_data = {}
    data=user_data.get(st.session_state.username)
    closest_diff=1000
    today_temp=st.session_state.temp_feel


    for date, evaluations in data.items():
            if ("体感温度" in evaluations):
                past_temp = float(evaluations["体感温度"])
                diff = abs(past_temp - today_temp)
                if diff < closest_diff:
                    closest_diff = diff
                    closest_record = evaluations
                    closest_date = date         
    st.subheader(f"最も近い服装の日とデータ: {closest_diff:.1f}℃")
    st.write(f"日付: {closest_date}")
    st.write("評価内容:")
    for key, value in closest_record.items():
        st.write(f"・{key}: {value}")
