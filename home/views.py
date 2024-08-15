from django.shortcuts import render
from django.http import JsonResponse
from io import BytesIO
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
from .weather import get_weather
from .priceplot import create_plot
from django.conf import settings
from django.utils import timezone
from datetime import datetime
import io
import base64
import mplcyberpunk
import matplotlib
matplotlib.use('Agg')
from home.models import SoilHealth
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SoilHealth
from .serializers import SoilHealthSerializer

class SoilHealthCreateView(APIView):
    def post(self, request):
        serializer  = SoilHealthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)










CITY_COORDINATES = {
    'Pratapgarh': {'lat': 25.9263, 'lon': 81.9864},
    
}

def info_view(request):
    city = 'Pratapgarh'  
    if 'city' in request.GET:
        city = request.GET['city']
    
    
    coordinates = CITY_COORDINATES.get(city, CITY_COORDINATES['Pratapgarh'])
    
    
    weather_data = get_weather(settings.WEATHER_API_KEY, coordinates['lat'], coordinates['lon'])
    
    
    price = create_plot()  
    
    
    soil_context = display_soil_data()
     
    soil_health_plot = generate_soil_health_plot()
    
    weather_data = get_weather_data(coordinates['lat'], coordinates['lon'], settings.WEATHER_API_KEY)
    temperature_plot = plot_temperatures(weather_data)
    
    context = {
        'weather': weather_data,
        'city': city,
        'price': price,
        'temperature_plot': temperature_plot,  
        'soil_health_plot': soil_health_plot,
        **soil_context  
    }
    
    return render(request, 'index.html', context)



def display_soil_data():
    
    recent_data = SoilHealth.objects.order_by('-date')[:7]
    
    data = {
        'date': [entry.date for entry in recent_data],
        'soil_moisture': [entry.soil_moisture for entry in recent_data],
        'soil_temperature': [entry.soil_temperature for entry in recent_data],
        'nitrogen_content': [entry.nitrogen_content for entry in recent_data],
        'phosphorus_content': [entry.phosphorus_content for entry in recent_data],
        'potassium_content': [entry.potassium_content for entry in recent_data],
        'soil_ph': [entry.soil_ph for entry in recent_data],
    }
    
    df = pd.DataFrame(data)
    
    
    df['date'] = pd.to_datetime(df['date'])
    
    latest_date = df['date'].max()
    is_today = latest_date.date() == timezone.now().date()
    numerical_data = df.to_dict(orient='records')

    today_data = df[df['date'] == latest_date].iloc[0] if not df[df['date'] == latest_date].empty else None
    
    if today_data is not None:
        today_categories = {
            'soil_moisture': categorize(today_data['soil_moisture'], [20, 25, 30]),
            'soil_temperature': categorize(today_data['soil_temperature'], [20, 22, 25]),
            'nitrogen_content': categorize(today_data['nitrogen_content'], [100, 110, 120]),
            'phosphorus_content': categorize(today_data['phosphorus_content'], [35, 40, 45]),
            'potassium_content': categorize(today_data['potassium_content'], [80, 85, 90]),
            'soil_ph': categorize(today_data['soil_ph'], [5.5, 6.0, 6.5]),
        }
        today_health = overall_health(today_categories)
    else:
        today_categories = {}
        today_health = "No Data"
    
    context = {
        'numerical_data': numerical_data,
        'today_health': today_health,
        'today_categories': today_categories,
        'is_today': is_today
    }
    
    return context


def categorize(value, thresholds):
    if value < thresholds[0]:
        return 'Worst'
    elif value < thresholds[1]:
        return 'Bad'
    elif value < thresholds[2]:
        return 'Good'
    else:
        return 'Best'

def overall_health(categories):
    worst_count = list(categories.values()).count('Worst')
    if worst_count > 1:
        return 'Worst'
    elif 'Worst' in categories.values():
        return 'Bad'
    elif 'Bad' in categories.values():
        return 'Good'
    else:
        return 'Best'
def generate_soil_health_plot():

    recent_data = SoilHealth.objects.order_by('-date')[:7]
    data = {
        'date': [entry.date for entry in recent_data],
        'soil_moisture': [entry.soil_moisture for entry in recent_data],
        'soil_temperature': [entry.soil_temperature for entry in recent_data],
        'nitrogen_content': [entry.nitrogen_content for entry in recent_data],
        'phosphorus_content': [entry.phosphorus_content for entry in recent_data],
        'potassium_content': [entry.potassium_content for entry in recent_data],
        'soil_ph': [entry.soil_ph for entry in recent_data],
    }

    df = pd.DataFrame(data)

    
    plt.figure(figsize=(14, 8))

    plt.plot(df['date'], df['soil_moisture'], label='Soil Moisture (%)', marker='o')
    plt.plot(df['date'], df['soil_temperature'], label='Soil Temperature (°C)', marker='o')
    plt.plot(df['date'], df['nitrogen_content'], label='Nitrogen Content (ppm)', marker='o')
    plt.plot(df['date'], df['phosphorus_content'], label='Phosphorus Content (ppm)', marker='o')
    plt.plot(df['date'], df['potassium_content'], label='Potassium Content (ppm)', marker='o')
    plt.plot(df['date'], df['soil_ph'], label='Soil pH', marker='o')

    plt.title('Soil Health Parameters Over Time')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    mplcyberpunk.add_glow_effects()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')

    return image_base64







def get_weather_data(lat, lon, api_key):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={api_key}&units=metric'
    response = requests.get(url)
    response.raise_for_status()  
    return response.json()
def plot_temperatures(weather_data):
    daily_data = weather_data.get('daily', [])
    
    if not daily_data or len(daily_data) < 7:
        print("Insufficient daily data available.")
        return None

    
    dates = []
    temps = []

    
    for day in daily_data[:7]:  
        date = datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d')
        temp_day = day['temp']['day']
        dates.append(date)
        temps.append(temp_day)

    buf = io.BytesIO()

    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker='o', linestyle='-', color='b')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature for Next 7 Days')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    
    plt.savefig(buf, format='png')
    buf.seek(0)  
    
    
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    buf.close()  
    
    return img_base64