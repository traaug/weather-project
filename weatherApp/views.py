import datetime
import json


import requests
from django.shortcuts import render


def weather_view(request):
    if request.method == 'POST':
        city = request.POST['city']
        api_key = '7c616a1600a07f879f1318bbd6049aae'
        base_url = 'https://api.openweathermap.org/data/2.5/'
        current_weather_endpoint = 'weather'
        forecast_endpoint = 'forecast'
        cnt = 5

        weather_url = f'{base_url}{current_weather_endpoint}?q={city}&units=metric&appid={api_key}'
        # forecast_url = f'{base_url}{forecast_endpoint}?q={city}&units=metric&cnt={cnt}&appid={api_key}'
        forecast_url = f'{base_url}{forecast_endpoint}?q={city}&units=metric&appid={api_key}'

        weather_response = requests.get(weather_url)
        forecast_response = requests.get(forecast_url)

        current_data = weather_response.json()
        forecast_data = forecast_response.json()

        if current_data['cod'] == 200 and forecast_data['cod'] == '200':
            current_weather = {
                'city': current_data['name'],
                'country': current_data['sys']['country'],
                'temperature': current_data['main']['temp'],
                'condition': current_data['weather'][0]['description'],
                'icon': current_data['weather'][0]['icon'],
            }

            forecast = []
            for day in forecast_data['list']:
                forecast.append({
                    'date': datetime.datetime.fromtimestamp(day['dt']).strftime('%A'),
                    'temperature': day['main']['temp'],
                    'condition': day['weather'][0]['description'],
                    'icon': day['weather'][0]['icon'],
                })

            return render(request, 'weatherApp/index.html', {'current_weather': current_weather, 'forecast': forecast})
        else:
            error_message = f'There is an error requiring your data. Status codes: Current: {current_data["cod"]}, ' \
                            f'Forecast: {forecast_data["cod"]}'
            print(f'Current Weather Response Content: {weather_response.content}')
            print(f'Forecast Response Content: {forecast_response.content}')
            return render(request, 'weatherApp/index.html', {'error_message': error_message})
    return render(request, 'weatherApp/index.html')
