import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import json
import creds



load_dotenv()
Weather_Endpoint = 'https://api.openweathermap.org/data/2.5/weather'
Weather_API_Key = os.getenv("WEATHER_API_KEY")
if not Weather_API_Key:
    raise ValueError("Weather API key is not set!")

city_lon = None
city_lat = None

city_name = input("Which city's weather do you want to know? : ")


with open("citys.json", "r",encoding="utf-8") as files:
    datas = json.load(files)

for data in datas:
    if data['name'].lower() == city_name.lower():
        city_lon = data['coord']['lon']
        city_lat = data['coord']['lat']
        break

if city_lat is None or city_lon is None:
    print("error")
else:
     weather_params = {
        "appid":Weather_API_Key,
        "lat": city_lat,
        "lon": city_lon,
        "units": "metric"
    }

response = requests.get(Weather_Endpoint, params=weather_params)
if response.status_code == 200:
    weather_data = response.json()
    print(f"Sehir: {city_name}")
    print(f"Hava: {weather_data['weather'][0]['description']} ve Sicaklik: {weather_data['main']['temp']} ")
else:
    print(f"Error !!! response code: {response.status_code}")