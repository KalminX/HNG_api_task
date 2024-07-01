import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import HelloSerializer

@api_view(['GET'])
def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = request.META.get('REMOTE_ADDR')
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')

    location_response = requests.get(f'https://ipinfo.io/{client_ip}/json?token=21714eb2148e07')
    location_data = location_response.json()
    location = location_data.get('city', 'Unknown')
    loc = location_data.get('loc', '0,0').split(',')
    lat, lon = loc[0], loc[1]

    # Fetch weather data
    weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=542ff3ea796cfa808e3731b2db89144c&units=metric')
    weather_data = weather_response.json()
    temperature = weather_data['main']['temp']

    data = {
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}",
    }

    serializer = HelloSerializer(data)
    return Response(serializer.data)
