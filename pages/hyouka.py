import json
import os

import streamlit as st
import time
from datetime import date

DATA_FILE = "user_data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        user_data = json.load(f)
else:
    user_data = {}

if "username" not in st.session_state:
    st.write("評価をするにはログインが必要です")
    new_user = st.text_input("あなたの名前を入力してください")

    # 新規登録確認の状態をsession_stateで管理
    if "new_user_not_found" not in st.session_state:
        st.session_state.new_user_not_found = False

    if st.session_state.new_user_not_found:
        st.write(f"{new_user}というユーザーが見当たりません。新規登録しますか？")
        if st.button("新規登録"):
            user_data[new_user] = {}  # 新規ユーザー登録（履歴用の空データ）
            with open(DATA_FILE, "w") as f:
                json.dump(user_data, f, indent=2)
            st.session_state.username = new_user
            st.session_state.new_user_not_found = False
            st.success(f"{new_user} として新規登録しました。ページを更新します...")
            time.sleep(2)
            st.rerun()
        if st.button("もう一度入力しなおす"):
            st.session_state.new_user_not_found = False
            st.rerun()
    else:
        if st.button("ログイン"):
            if new_user in user_data:
                st.session_state.username = new_user
                # st.success(f"{new_user} としてログインしました")
                st.rerun()
            else:
                st.session_state.new_user_not_found = True
                st.rerun()
else:
    st.sidebar.success(f"{st.session_state.username} さんとしてログイン中")
    if st.sidebar.button("ログアウト"):
        del st.session_state.username
        st.rerun()
    today = date.today()
    today_str = str(today)

    jacket = "上着"
    tops = "トップス"
    bottoms = "ボトムス"
    winter_clothes = "防寒具"

    evaluate = {}
    # evaluate["日付"] = today

    st.title("評価")
    col1 , col2 , col3 , col4, col5 = st.columns(5)
    with col1:
        st.write(jacket)
        option1=["なし","薄手","厚手",]
        evaluate[jacket] = st.selectbox(jacket,option1)
    with col2:
        st.write(tops)
        option2=["半袖","長袖","厚手の長袖",]
        evaluate[tops] = st.selectbox(tops,option2)
    with col3:
        st.write(bottoms)
        option3=["短パン","長ズボン","厚手の長ズボン",]
        evaluate[bottoms] = st.selectbox(bottoms,option3)
    with col4:
        st.write(winter_clothes)
        option4=["なし","手袋","マフラー","手袋&マフラー"]
        evaluate[winter_clothes] = st.selectbox(winter_clothes,option4)
    with col5:
        st.write("気温")
        evaluate["評価"] = st.radio("これを…", ("暑かった", "寒かった", "ちょうどいい"))

    # if st.button("保存"):
    #     user_data[st.session_state.username][today] = evaluate
    #     with open(DATA_FILE, "w") as f:
    #         json.dump(user_data, f, indent=2)
    #     st.subheader("フィードバックを受け付けました！")
    #     for category, choice in evaluate.items():
    #         st.write(f"・{category}：{choice}")

    
    if st.button("保存"):
        user_data[st.session_state.username][today_str] = evaluate
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        st.subheader("フィードバックを受け付けました！")
        for category, choice in evaluate.items():
            st.write(f"・{category}：{choice}")
