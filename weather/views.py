from django.shortcuts import render
import json
import urllib.request
from datetime import datetime,timedelta
from .models import WeatherAlert
from .forms import WeatherAlertForm
import os
# Replace with your OpenWeatherMap API key
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
def index(request):
    data = {}
    if request.method == 'POST':
        city = request.POST.get('city', '')
        if city:
            data = get_weather_data(city)[0]  # Assuming get_weather_data returns (weather_data, forecast_list)
    
    return render(request, 'index.html', {'data': data})


def get_weather_data(city):
    weather_data = {}
    forecast_list = []

    try:
        # Current Weather Data
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        weather_response = urllib.request.urlopen(weather_url).read()
        weather_data = json.loads(weather_response)

        if 'main' in weather_data and 'weather' in weather_data:
            weather_data = {
                "city": weather_data['name'],
                "temp_celsius": weather_data['main']['temp'],
                "feels_like_celsius": weather_data['main']['feels_like'],
                "pressure": weather_data['main']['pressure'],
                "humidity": weather_data['main']['humidity'],
                "wind_speed": weather_data['wind']['speed'],
                "description": weather_data['weather'][0]['description'].capitalize(),
                "icon": weather_data['weather'][0]['icon'],
            }

        # 5-Day/3-Hour Forecast Data
        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        forecast_response = urllib.request.urlopen(forecast_url).read()
        forecast_data = json.loads(forecast_response)

        if 'list' in forecast_data:
            for forecast in forecast_data['list']:
                forecast_list.append({
                    "date": forecast['dt_txt'].split(' ')[0],
                    "time": forecast['dt_txt'].split(' ')[1],
                    "temp": forecast['main']['temp'],
                    "feels_like": forecast['main']['feels_like'],
                    "pressure": forecast['main']['pressure'],
                    "humidity": forecast['main']['humidity'],
                    "description": forecast['weather'][0]['description'].capitalize(),
                    "icon": forecast['weather'][0]['icon'],
                    "wind_speed": forecast['wind']['speed'],
                    "wind_direction": forecast['wind'].get('deg', 'N/A'),
                    "cloudiness": forecast['clouds']['all'],
                    "visibility": forecast.get('visibility', 'N/A')
                })

    except Exception as e:
        print(f"Error fetching weather data: {e}")

    return weather_data, forecast_list


def forecast(request):
    city = request.POST.get('city', '')
    forecast_list = []

    if city:
        weather_data, forecasts = get_weather_data(city)
        
        if forecasts:
            forecast_list = forecasts

    return render(request, 'forecast.html', {
        'city': city,
        'forecast_list': forecast_list,
    })


def get_weather_alerts(city):
    # Example: generating mock data with realistic time differences
    current_time = datetime.now()
    
    # Storm Alert
    storm_alert_start = current_time + timedelta(hours=1, minutes=30)
    storm_alert_end = storm_alert_start + timedelta(hours=2)
    
    # Heat Wave Warning
    heat_wave_start = current_time + timedelta(days=1, hours=2)
    heat_wave_end = heat_wave_start + timedelta(hours=3)
    
    alerts = [
        WeatherAlert(event='Storm Alert', start=storm_alert_start, end=storm_alert_end, description='Storm approaching'),
        WeatherAlert(event='Heat Wave Warning', start=heat_wave_start, end=heat_wave_end, description='High temperatures expected')
    ]
    return alerts

def weather_alerts(request):
    if request.method == 'POST':
        form = WeatherAlertForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            alerts = get_weather_alerts(city)  # Replace with your function to fetch weather alerts
            return render(request, 'weather_alerts.html', {'form': form, 'alerts': alerts})
    else:
        form = WeatherAlertForm()
    
    return render(request, 'weather_alerts.html', {'form': form})


def air_quality(request):
    if request.method == 'POST':
        city = request.POST.get('city', '')
        air_quality_index = {}

        try:
            if city:
                weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
                weather_response = urllib.request.urlopen(weather_url).read()
                weather_data = json.loads(weather_response)

                if 'coord' in weather_data:
                    coord = weather_data['coord']
                    air_quality_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={coord["lat"]}&lon={coord["lon"]}&appid={API_KEY}'
                    air_quality_response = urllib.request.urlopen(air_quality_url).read()
                    air_quality_data = json.loads(air_quality_response)
                    if 'list' in air_quality_data and len(air_quality_data['list']) > 0:
                        air_quality_index = {
                            "aqi": air_quality_data['list'][0]['main']['aqi'],
                            "components": air_quality_data['list'][0]['components']
                        }

        except Exception as e:
            print(f"Error fetching air quality data: {e}")

        return render(request, 'air_quality.html', {
            'city': city,
            'air_quality_index': air_quality_index,
        })

    return render(request, 'air_quality.html')

def interactive_maps(request):
    return render(request, 'interactive_maps.html')

