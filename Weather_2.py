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

        if len(temps_today) == 2:
            st.subheader(f"📅 今日（{today.strftime('%m月%d日')}）の体感温度")
            for hour in sorted(temps_today):
                dt, tm = temps_today[hour]
                st.markdown(f"### {dt.strftime('%H:%M')} の体感温度：`{tm:.2f} °C`")
        elif len(temps_today) == 1:
            st.subheader(f"📅 今日（{today.strftime('%m月%d日')}）の体感温度")
            for hour in sorted(temps_today):
                dt, tm = temps_today[hour]
                st.markdown(f"### {dt.strftime('%H:%M')} の体感温度：`{tm:.2f} °C`")
                if temps_tomorrow:
                    st.subheader(f"📅 明日（{tomorrow.strftime('%m月%d日')}）の体感温度")
                    dt, tm = temps_tomorrow[12]
                    st.markdown(f"### {dt.strftime('%H:%M')} の体感温度：`{tm:.2f} °C`")
        else:
            st.warning("今日の12時または18時の体感温度が取得できませんでした。")
            if temps_tomorrow:
                st.subheader(f"📅 明日（{tomorrow.strftime('%m月%d日')}）の体感温度")
                for hour in sorted(temps_tomorrow):
                    dt, tm = temps_tomorrow[hour]
                    st.markdown(f"### {dt.strftime('%H:%M')} の体感温度：`{tm:.2f} °C`")
            else:
                st.error("明日の12時・18時の体感温度も取得できませんでした。")
else:
    st.error("位置情報が取得できませんでした。別の都道府県を選んでください。")
