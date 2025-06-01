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

