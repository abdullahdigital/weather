from django.db import models

class WeatherAlert(models.Model):
    city = models.CharField(max_length=100)
    event = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return f"{self.city} - {self.event}"
