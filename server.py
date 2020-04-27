import requests, json
from flask import Flask, render_template, url_for, redirect, request
from secret import api_key
import sys, time, os
from  geopy.geocoders import Nominatim

# Section - API
lon = '45.50'
lat = '73.57'

unit_format = {
    'Fahrenheit' : 'imperial',
    'Celsius' : 'metric'
}

global unit
unit = unit_format["Celsius"]

# Weather API
api_call = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units={unit}&appid={api_key}'
response = requests.get(api_call)

# Flask Param
lan = True
IP = '0.0.0.0'
app = Flask(__name__)

# Section - Classes

# Class - Visual Weather
class VisualWeatherFormat():
    def __init__(self, description, icon, id, main):
        self.description = description
        self.icon = icon
        self.id = id
        self.main = main

# Class - Feels Like
class WeatherFeelsLike():
    def __init__(self, day, eve, morn, night):
        self.day = int(day)
        self.evening = int(eve)
        self.morning = int(morn)
        self.night = int(night)

# Class - General Weather
class GeneralWeather():
    def __init__(self, clouds, dew_point, humidity, wind_speed):
        self.clouds = clouds
        self.dew_point = dew_point
        self.humidity = humidity
        self.wind_speed = wind_speed

# Section - Unrealated Functions
def verify_connection(response):
    connection_code = response.status_code
    print("")
    print(f"[*] Verifying Connection to the API")
    if connection_code == 200:
        print("")
        print("[*] Connection Established - {}".format(connection_code))
        return 'API Connected'
    elif connection_code == 404:
        return "Unkown API Error - {}".format(connection_code)
    else:
        return "Unkown API Error - {}".format(connection_code)

def visual_weather_data(id, weather):
    #base_url = 'http://openweathermap.org/img/wn/{}@2x.png'.format(icon)
    print("")
    print("[*] Grabbing Weather Information")

    # Weather Data - Dict
    Weather = {
        'Thunderstorm' : {
            200 : 'thunderstorm with light rain',
            201 : 'thunderstorm with rain',
            202 : 'thunderstorm with heavy rain',
            210 : 'thunderstorm with heavy rain',
            211 : 'thunderstorm',
            212 : 'heavy thunderstorm',
            221 : 'ragged thunderstorm',
            230 : 'thunderstorm with light drizzle',
            231 : 'thunderstorm with drizzle',
            232 : 'thunderstorm with heavy drizzle'
        },
        'Drizzle' : {
            300 : 'light intensity drizzle',
            301 : 'drizzle',
            302 : 'heavy intensity drizzle',
            310 : 'light intensity drizzle rain',
            311 : 'drizzle rain',
            312 : 'heavy intensity drizzle rain',
            313 : 'shower rain and drizzle',
            314 : 'heavy shower rain and drizzle',
            321 : 'shower drizzle'
        },
        'Rain' : {
            500 : 'light rain',
            501 : 'moderate rain',
            502 : 'heavy intensity rain',
            503 : 'very heavy rain',
            504 : 'extreme rain',
            511 : 'freezing rain',
            520 : 'light intensity shower rain',
            521 : 'shower rain',
            522 : 'heavy intensity shower rain',
            531 : 'ragged shower rain'
        },
        'Snow' : {
            600 : 'light snow',
            601 : 'Snow',
            602 : 'Heavy snow',
            611 : 'Sleet',
            612 : 'Light shower sleet',
            613 : 'Shower sleet',
            615 : 'Light rain and snow',
            616 : 'Rain and snow',
            620 : 'Light shower snow',
            621 : 'Shower snow',
            622 : 'Heavy shower snow'
        },
        'Atmosphere' : {
            701 : 'mist',
            711 : 'Smoke',
            721 : 'Haze',
            731 : 'Dust',
            741 : 'Fog',
            751 : 'Sand',
            761 : 'Dust',
            771 : 'Squall',
            781 : 'Tornado'
        },
        'Clear' : {
            800 : 'Clear Sky'
        },
        'Clouds' : {
            801 : 'few clouds: 11-25%',
            802 : 'scattered clouds: 25-50%',
            803 : 'broken clouds: 51-84%',
            804 : 'overcast clouds: 85-100%'
        }
    }
    try: 
        return Weather[weather][id]
    except (IndexError, KeyError) as method:
        return Weather['Atmosphere'][id]

@app.route('/error')
def error_handler(message):
    print("")
    print(f"[x] Error - {message} ")
    return render_template('error.html', message=message)

# Flask Routing

# Flask Routing - homepage
@app.route('/')
def home():

    connection_weather = verify_connection(response)

    if connection_weather == 'API Connected':
        try:
            # -- Request Information to Grab --
            visual_weather_format = VisualWeatherFormat(
                response.json()['daily'][0]['weather'][0]['description'],
                response.json()['daily'][0]['weather'][0]['icon'],
                response.json()['daily'][0]['weather'][0]['id'],
                response.json()['daily'][0]['weather'][0]['main']
            )

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
            # -- Request Information to Grab --

            forcast = visual_weather_data(visual_weather_format.id, visual_weather_format.main)
            weather_icon = visual_weather_format.icon
            weather_icon = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
            print("")
            print(f'[*] Forcast - {forcast}')
            print("")
            print(f"[*] Weather Icon - {weather_icon}")
            print(feels_like.day)
            return render_template('index.html', forcast=forcast, weather_icon=weather_icon, feels_like=feels_like, general_weather=general_weather)
        except:
            return render_template('error.html', message="An unknown error occured")
    else:
        return render_template('error.html', message=connection)

# Flask Routing - Specific Location
@app.route('/weather/<string:user_location>')
def update_location(user_location):
    geolocator = Nominatim()
    location = user_location.split(',')
    city = location[0]
    country = location[1]
    loc = geolocator.geocode(city+','+ country)

    lon = loc.longitude
    lat = loc.latitude
    api_call = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units={unit}&appid={api_key}'
    response = requests.get(api_call)
    connection_weather = verify_connection(response)

    if connection_weather == 'API Connected':
        try:

            # -- Request Information to Grab --
            visual_weather_format = VisualWeatherFormat(
                response.json()['daily'][0]['weather'][0]['description'],
                response.json()['daily'][0]['weather'][0]['icon'],
                response.json()['daily'][0]['weather'][0]['id'],
                response.json()['daily'][0]['weather'][0]['main']
            )

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
                response.json()['daily'][0]['wind_speed'],  
            )
            # -- Request Information to Grab --

            forcast = visual_weather_data(visual_weather_format.id, visual_weather_format.main)
            weather_icon = visual_weather_format.icon
            weather_icon = f'http://openweathermap.org/img/wn/{weather_icon}@2x.png'
            print("")
            print(f'[*] Forcast - {forcast}')
            print("")
            print(f"[*] Weather Icon - {weather_icon}")

            return render_template('index.html', forcast=forcast, weather_icon=weather_icon, feels_like=feels_like, general_weather=general_weather)
        except:
            return render_template('error.html', message="An unknown error occured")
    else:
        return render_template('error.html', message=connection)


@app.route('/weather_update', methods=['POST', 'GET'])
def weather_update():
    if request.method == 'POST':
        data = request.form.to_dict()
        print("")
        print("[*] New Location - {}".format(data['location']))
        user_location = data['location']
        return redirect(url_for('update_location', user_location=user_location))
        #return resp_json_payload['results'][0]['geometry']['location']

if __name__ == '__main__':
    try:
        print("")
        print("-- Backend --")
        
        if lan:
            app.run()
        else:
            app.run(host=IP)
    except (KeyboardInterrupt) as reason:
        error_handler(reason)