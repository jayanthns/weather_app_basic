import json
from pathlib import Path
import requests
from typing import Any, Dict, List

import geocoder

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import CitySerializer
from .models import City

CITIES_JSON_FILE_PATH = Path("./cities.json")
OPEN_WEATHER_APP_KEY = "9e3443b81efb6665ca6a2bb41d536ff5"
OPEN_WEATHER_CURRENT_DETAILS_API = f"https://api.openweathermap.org/data/2.5/weather?appid={OPEN_WEATHER_APP_KEY}&q="
OPEN_WEATHER_FORECAST_DETAILS_API = f"https://api.openweathermap.org/data/2.5/forecast?appid={OPEN_WEATHER_APP_KEY}&q="
DEFAULT_CITY = "Kuala Lumpur"

city_response = openapi.Response('response description', CitySerializer)

city_param = openapi.Parameter('cities', openapi.IN_QUERY, description="city names comma separated. ex: 'bengaluru, mysuru'", type=openapi.TYPE_STRING)
forecast_param = openapi.Parameter('forecast', openapi.IN_QUERY, description="show foreacast data", type=openapi.TYPE_INTEGER, default=0)



# Create your views here.


def _get_city_names() -> List[str]:
    """prepare list of city names from the json file"""
    with open(CITIES_JSON_FILE_PATH, "r") as read_file:
        return [city['city'] for city in json.loads(read_file.read())]


def _get_current_weather(city: str) -> Dict[str, Any]:
    """
    fetch the current weather for the provided city
    """
    url = f"{OPEN_WEATHER_CURRENT_DETAILS_API}{city}"
    res = requests.get(url)
    weather = res.json()['weather'][0]
    weather['city'] = city
    return weather


def _get_forecast_weather(city: str) -> Dict[str, Any]:
    """
    fetch the forecast weather data for the provided city
    """
    url = f"{OPEN_WEATHER_FORECAST_DETAILS_API}{city}"
    res = requests.get(url)
    print(url)
    print(res.status_code)
    # print(res.json())
    weathers = [weather['weather'][0] for weather in res.json()['list'][:5]]
    return weathers


@swagger_auto_schema(method="get", manual_parameters=[city_param, forecast_param], responses={200: {}})
@api_view(['GET'])
def weather_by_city(request: Request) -> Response:
    """
    fetch the weather for the requested city name, otherwise
    send the details of the default city 'Kuala Lumpur'
    """
    cities = request.GET.get('cities', DEFAULT_CITY).split(",")
    forecast = request.GET.get('forecast', 0)
    print(forecast)

    if not forecast == 1:
        return Response([_get_current_weather(city) for city in cities])
    return Response({"city": city, "forecast_data": _get_forecast_weather(city)} for city in cities)

@api_view(['GET'])
def current_location_weather(request: Request) -> Response:
    """
    fetch the current weather opf the current location
    """
    current_location = geocoder.ip('me')
    current_city = current_location.current_result.city
    return Response(_get_current_weather(current_city))


@api_view(['GET'])
def cities(request: Request) -> Response:
    """
    Api for getting the cities.
    This api allows only get request
    """
    my_cities = City.objects.values_list('city_name', flat=True)
    return Response([*_get_city_names(), *my_cities])

@swagger_auto_schema(methods=['post'], request_body=CitySerializer)
@api_view(['POST'])
def add_city(request: Request) -> Response:
    """
    APi to create or adding new city
    """
    serializer = CitySerializer(data=request.data)
    if serializer.is_valid():
        return Response(CitySerializer(serializer.save()).data)

    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
