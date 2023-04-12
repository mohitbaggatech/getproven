from django.db import models
from datetime import datetime

DETAILING_TYPES = [
    ("C", "Current"),
    ("M", "Minutely"),
    ("H", "Hourly"),
    ("D", "Daily")
]

class Location(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    created = models.DateTimeField(blank=True, auto_now_add=True)
    updated = models.DateTimeField(blank=True, auto_now=True)
    
    
class WeatherForecast(models.Model):
    location = models.ForeignKey(Location, null=False, blank=False, on_delete=models.DO_NOTHING)
    detailing = models.CharField(max_length=1, choices=DETAILING_TYPES)
    weather_data = models.JSONField()
    created = models.DateTimeField(blank=True, auto_now_add=True)
    updated = models.DateTimeField(blank=True, auto_now=True)
