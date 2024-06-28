from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('forecast/', views.forecast, name='forecast'),
     path('weather_alerts/', views.weather_alerts, name='weather_alerts'),
    path('air_quality/', views.air_quality, name='air_quality'),
    path('maps/', views.interactive_maps, name='interactive_maps'),
]
