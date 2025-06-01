import streamlit as st
import requests

import streamlit as st
import requests
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim



# 🔑 OpenWeatherMap APIキーを入力
API_KEY = "129959c8cc98ea896a4b7ccfabefdbca"

st.set_page_config(page_title="体感温度（都道府県）", page_icon="🗾")
st.title("🗾 都道府県を選んで体感温度を表示")

# ✅ 都道府県リスト
prefectures = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
    "岐阜県", "静岡県", "愛知県", "三重県",
    "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
    "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県",
    "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

# ✅ 都道府県を選択
pref = st.selectbox("都道府県を選択してください", prefectures)

# ✅ geopyで緯度経度を取得（403対策済み）
geolocator = Nominatim(user_agent="my_streamlit_app (your@email.com)")
location = geolocator.geocode(pref)

if location:
    lat, lon = location.latitude, location.longitude
    st.success(f"{pref} の緯度: {lat:.4f}, 経度: {lon:.4f}")

    # 🌤 OpenWeatherMapから予報取得
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=ja"
    res = requests.get(url)

    if res.status_code != 200:
        st.error("天気情報の取得に失敗しました。")
    else:
        data = res.json()
        target_hours = [12, 18]
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        def extract_temperatures(for_date):
            temps = {}
            for entry in data["list"]:
                dt = datetime.fromtimestamp(entry["dt"])
                if dt.date() == for_date and dt.hour in target_hours and dt.hour not in temps:
                    t = entry["main"]["temp"]
                    h = entry["main"]["humidity"]
                    v = entry["wind"]["speed"]
                    A = 1.76 + 1.4 * v**0.75
                    Tm = 37 - (37 - t) / (0.68 - 0.0014 * h + 1 / A) - 0.29 * t * (1 - h / 100)
                    temps[dt.hour] = (dt, Tm)
            return temps

        temps_today = extract_temperatures(today)
        temps_tomorrow = extract_temperatures(tomorrow)
        temp_list=[]
        if len(temps_today) == 2:
            for hour in sorted(temps_today):
                dt, tm = temps_today[hour]
                temp_list.append((dt,tm))
        elif len(temps_today) == 1:
            for hour in sorted(temps_today):
                dt, tm = temps_today[hour]
                temp_list.append((dt,tm))
                if temps_tomorrow:
                    dt, tm = temps_tomorrow[12]
                    temp_list.insirt(0,(dt,tm))
        else:
            st.warning("12時または18時の体感温度が取得できませんでした。")
            if temps_tomorrow:
                for hour in sorted(temps_tomorrow):
                    dt, tm = temps_tomorrow[hour]
            else:
                st.error("明日の12時・18時の体感温度も取得できませんでした。")
else:
    st.error("位置情報が取得できませんでした。別の都道府県を選んでください。")




url1="https://cdn.pixabay.com/photo/2020/01/29/17/09/snowboard-4803050_1280.jpg"
url2="https://cdn.pixabay.com/photo/2021/03/08/18/16/man-6079789_1280.jpg"
url3="https://cdn.pixabay.com/photo/2017/11/05/15/44/man-2920911_1280.jpg"
url4="https://cdn.pixabay.com/photo/2022/12/27/20/39/man-7681763_1280.jpg"
url5="https://cdn.pixabay.com/photo/2016/11/29/07/16/balancing-1868051_1280.jpg"
url6="https://cdn.pixabay.com/photo/2020/06/20/16/13/male-5321547_1280.jpg"

url_list=[url1,url2,url3,url4,url5,url6]#寒い順に画像のurl
url_day=url6
url_mornig=url6
Tm_day=temp_list[1][1]
Tm_morning=temp_list[0][1]
temp=[0,5,10,15,20,25]#基準となる気温
for i in range(6):
    if(Tm_day<temp[i]):
     url_day=url_list[i]
     break

for i in range(6):
    if(Tm_morning<temp[i]):
     url_morning=url_list[i]
     break


st.title("今日の服装")
Tm = st.session_state.Tm_day

st.metric("体感温度 (°C)", f"{Tm:.2f} °C")

col1, col2 = st.columns(2)  
with col1:
    st.write("朝夜の服装")
    st.image(url_morning)

with col2:
    st.write("日中の服装")
    st.image(url_day)