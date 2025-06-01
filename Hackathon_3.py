import requests

# 現在地の緯度・経度をIPアドレスから取得
location = requests.get("http://ip-api.com/json/").json()
lat = location["lat"]
lon = location["lon"]

# OpenWeather API情報
API_KEY = '129959c8cc98ea896a4b7ccfabefdbca'
UNITS = 'metric'
LANG = 'ja'

# OpenWeatherから天気を取得
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={UNITS}&lang={LANG}"
response = requests.get(url)
data = response.json()

# 天気データから体感温度を計算
if response.status_code == 200:
    t = data['main']['temp']         # 気温
    h = data['main']['humidity']     # 湿度
    v = data['wind']['speed']        # 風速

    A = 1.76 + 1.4 * v**0.75
    Tm = 37 - (37 - t) / (0.68 - 0.0014 * h + 1/A) - 0.29 * t * (1 - h / 100)

    print(f"現在地: {location['city']}, {location['regionName']}")
    print(f"気温: {t}°C, 湿度: {h}%, 風速: {v}m/s")
    print(f"体感温度: {Tm:.2f} °C")
else:
    print(f"エラー: {data['message']}")
