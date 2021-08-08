from django.urls import path

from .views import add_city, cities, current_location_weather, weather_by_city

urlpatterns = [
    path('', view=weather_by_city, name="weather_city"),
    path('cities/', view=cities, name="cities"),
    path('current_city/', view=current_location_weather, name="current_city_weather"),
    path('add_city/', view=add_city, name="add_city"),
]
