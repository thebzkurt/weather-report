import tkinter
from tkinter import Canvas, ttk
import requests
from dotenv import load_dotenv
import os
import json
from tkinter import *
from PIL import Image, ImageTk


load_dotenv()
Weather_Endpoint = 'https://api.openweathermap.org/data/2.5/weather'
Weather_API_Key = os.getenv("WEATHER_API_KEY")
if not Weather_API_Key:
    raise ValueError("Weather API key is not set!")

city_lon = None
city_lat = None
selected_city = None

#--------------------------------  foksiyonlar  --------------------------------#

def get_value():
    global city_lon, city_lat, selected_city
    selected_city = city_combobox.get()
    print(f'Secilen sehir: {selected_city}')


#--------------------------------  json dosyasindan veri alinimi  --------------------------------#
    try:
        with open("citys.json", "r",encoding="utf-8") as files:

            datas = json.load(files)

            for data in datas:
                if data['name'].lower() == selected_city:
                    city_lon = data['coord']['lon']
                    city_lat = data['coord']['lat']
                    break

            if city_lat is None or city_lon is None:
                result_label.config(text="Error Sehir bulunamadi.")
                return
    except FileNotFoundError:
        result_label.config(text="Error: 'citys.json' dosyasi bulunamadi")
        return

    weather_params = {
        "appid":Weather_API_Key,
        "lat": city_lat,
        "lon": city_lon,
        "units": "metric"
    }

#--------------------------------  kodun son asamasi  --------------------------------#

    response = requests.get(Weather_Endpoint, params=weather_params)
    if response.status_code == 200:
        weather_data = response.json()
        print(f"Sehir: {selected_city}")
        print(f"Hava: {weather_data['weather'][0]['description']} ve Sicaklik: {weather_data['main']['temp']} ")
        result_label.config(
            text=f"{selected_city} : Hava Durumu: {weather_data['weather'][0]['description']}\nSicaklik: {weather_data['main']['temp']}")
    else:
        print(f"Error !!! response code: {response.status_code}")

#--------------------------------  arayuz olusturma  --------------------------------#

window = Tk()
window.title("Hava Durumu")
window.config(background="gray",padx=10,pady=10)

canvas = Canvas(window, height=120, width=120,bg="gray",bd=0)
logo_img = PhotoImage(file="images/weather-app (1).png")
canvas.create_image(60,60,image=logo_img)
canvas.grid(row=0,column=0,columnspan=2)

city_combobox = ttk.Combobox(window,values=["konya","istnabul","ankara","yozgat"],state="readonly")
city_combobox.set("Sehir sec")
city_combobox.grid(row=2,column=0)

city_button = tkinter.Button(window, text=("Hava Durumunu Goster"), command=get_value)
city_button.grid(row=2,column=1)

result_label = tkinter.Label(window, text="",font=("Arial", 12),bg= "gray")
result_label.grid(row=1,column=0,columnspan=2)



window.mainloop()


