import requests, json
from flask import Flask, render_template, url_for, redirect
from secret import api_key
import sys, time, os

# Web - Info
global css_static
global js_static

css_static = './static/css/style.css'
js_static = './static/js/app.js'

lan = True
IP = '0.0.0.0'
app = Flask(__name__)

# API - Info
test_lon = '45.50'
test_lat = '73.57'

unit_format = {
    'Fahrenheit' : 'imperial',
    'Celsius' : 'metric'
}

unit = unit_format["Celsius"]
api_call = f'https://api.openweathermap.org/data/2.5/onecall?lat={test_lat}&lon={test_lon}&units={unit}&appid={api_key}'
response = requests.get(api_call)

# Class - 1 - WeatherFeelsLike
class WeatherFeelsLike():
    def __init__(self, day, eve, morn, night):
        self.day = int(day)
        self.evening = int(eve)
        self.morning = int(morn)
        self.night = int(night)

# Class - 2 - GeneralWeather
class GeneralWeather():
    def __init__(self, clouds, dew_point, humidity, pressure):
        self.clouds = clouds
        self.dew_point = dew_point
        self.humidity = humidity
        self.pressure = pressure

# Class - 3 - VisualWeatherFormat
class VisualWeatherFormat():
    def __init__(self, description, icon, id, main):
        self.description = description
        self.icon = icon
        self.id = id
        self.main = main

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


# -- Grabbing Weather Info from JSON --
feels_like = WeatherFeelsLike(
    response.json()['daily'][0]["feels_like"]['day'],
    response.json()['daily'][0]["feels_like"]['eve'],
    response.json()['daily'][0]["feels_like"]['morn'],
    response.json()['daily'][0]["feels_like"]['night']               
)

general_weather = GeneralWeather(
    response.json()['daily'][0]['clouds'],
    response.json()['daily'][0]['dew_point'],
    response.json()['daily'][0]['humidity'],
    response.json()['daily'][0]['pressure'],  
)

visual_weather_format = VisualWeatherFormat(
    response.json()['daily'][0]['weather'][0]['description'],
    response.json()['daily'][0]['weather'][0]['icon'],
    response.json()['daily'][0]['weather'][0]['id'],
    response.json()['daily'][0]['weather'][0]['main']
)
# -- Grabbing Weather Info from JSON --

class FiveDayFormat():
    def __init__(self, icon, temp, feels_like):
        self.icon = icon
        self.temp = temp
        self.feels_like = feels_like

for day in range(6):
    'five_day_forcast_{day}'.format(day) = FiveDayFormat(
        response.json()['daily'][day]['weather'][0]['icon'],
        response.json()['daily'][day]['temp']['day'],
        response.json()['daily'][day]['feels_like']['day']
    )


print(five_day_forcast_1.icon)

#jprint(response.json()['daily'])
#rint(response.json())