import streamlit as st
import requests

# 現在地をIPから取得
def get_location():
    res = requests.get("http://ip-api.com/json/").json()
    return res['lat'], res['lon'], res['city'], res['regionName']

# 天気情報をOpenWeatherから取得
def get_weather(lat, lon, api_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ja'
    res = requests.get(url)
    return res.json()

# 体感温度を計算
def calc_apparent_temp(t, h, v):
    A = 1.76 + 1.4 * v**0.75
    Tm = 37 - (37 - t) / (0.68 - 0.0014 * h + 1/A) - 0.29 * t * (1 - h / 100)
    return Tm

# Streamlit UI
st.title("🌤 現在地の天気情報")

API_KEY = "129959c8cc98ea896a4b7ccfabefdbca"

lat, lon, city, region = get_location()
data = get_weather(lat, lon, API_KEY)

if data.get("main"):
    t = data["main"]["temp"]
    h = data["main"]["humidity"]
    v = data["wind"]["speed"]
    Tm = calc_apparent_temp(t, h, v)

    st.subheader(f"📍 {region} - {city}")
    st.metric("体感温度 (°C)", f"{Tm:.2f} °C")
else:
    st.error("天気情報を取得できませんでした。")


url1="https://cdn.pixabay.com/photo/2020/01/29/17/09/snowboard-4803050_1280.jpg"
url2="https://cdn.pixabay.com/photo/2021/03/08/18/16/man-6079789_1280.jpg"
url3="https://cdn.pixabay.com/photo/2017/11/05/15/44/man-2920911_1280.jpg"
url4="https://cdn.pixabay.com/photo/2022/12/27/20/39/man-7681763_1280.jpg"
url5="https://cdn.pixabay.com/photo/2016/11/29/07/16/balancing-1868051_1280.jpg"
url6="https://cdn.pixabay.com/photo/2020/06/20/16/13/male-5321547_1280.jpg"

url_list=[url1,url2,url3,url4,url5,url6]#寒い順に画像のurl
url=url6
temp=[0,5,10,15,20,25]
for i in range(6):
    if(Tm<temp[i]):
     url=url_list[i]
     break



st.title("今日の服装")
col1, col2 = st.columns(2)  
with col1:
    st.write("朝夜の服装")
    st.image(url)

with col2:
    st.write("日中の服装")
    st.image(url)

