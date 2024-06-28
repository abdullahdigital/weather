from django.contrib import admin
from .models import WeatherAlert  # Import the model

admin.site.register(WeatherAlert)  # Register the model with the admin interface
