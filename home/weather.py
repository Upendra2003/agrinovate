import requests

def get_weather(api_key, lat, lon):
    base_url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric',  
        'exclude': 'minutely,hourly'  
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return None
