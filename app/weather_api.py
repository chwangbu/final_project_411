import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_current_weather(city):
    response = requests.get(f"{BASE_URL}/weather", params={
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    })
    return response.json()

def get_forecast(city):
    response = requests.get(f"{BASE_URL}/forecast", params={
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    })
    return response.json()

def get_historical_weather(lat, lon, timestamp):
    response = requests.get(f"{BASE_URL}/onecall/timemachine", params={
        "lat": lat,
        "lon": lon,
        "dt": timestamp,
        "appid": API_KEY,
        "units": "metric"
    })
    return response.json()