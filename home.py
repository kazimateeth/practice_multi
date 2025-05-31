import streamlit as st

st.title("今日の服装")
col1, col2 = st.columns(2)  
with col1:
    st.write("朝夜の服装")
    st.image("https://cdn.pixabay.com/photo/2021/03/08/18/16/man-6079789_1280.jpg")

with col2:
    st.write("日中の服装")
    st.image("https://cdn.pixabay.com/photo/2020/06/20/16/13/male-5321547_1280.jpg")

