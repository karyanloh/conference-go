from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
import json

def get_photo(city, state):
    url = "https://api.pexels.com/v1/search"
    headers = {'Authorization':PEXELS_API_KEY}
    params = {
        "per_page" : 1,
        "query": city + "," + state,
    }
    response = requests.get(url, params=params, headers=headers)

    pic = json.loads(response.content)

    try:
        return {'picture_url': pic['photos'][0]['src']['original']}
    except (KeyError, IndexError):
        return {'picture_url': None}

def get_weather(city, state):
    # print(f'GET Weather Triggered')
    #translate city state into geocode
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        'q' : f'{city}, {state}, US',
        'limit': 1,
        'appid': OPEN_WEATHER_API_KEY
    }
    response = requests.get(url, params=params)
    content = json.loads(response.content)

    try:
        lat = content[0]['lat']
        lon = content[0]['lon']
    except (KeyError, IndexError):
        return None

    #get weather from geocode
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPEN_WEATHER_API_KEY,
        'units': 'imperial'
    }
    response = requests.get(url, params=params)
    content = json.loads(response.content)
    try:
        return {
            'description': content['weather'][0]['description'],
            'temperature': content['main']['temp'],
        }
    except (KeyError, IndexError):
        return None
