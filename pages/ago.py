import streamlit as st

st.write("過去の服装")
col1 , col2 =st.columns(2)
with col1:
 st.image("https://cdn.pixabay.com/photo/2021/03/08/18/16/man-6079789_1280.jpg")
with col2:
 st.write("暑かった")
