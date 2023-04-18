from django.shortcuts import render
from weather.forms import LocationForm
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from weather.cloud_third_party import WeatherAPI
from weather.models import WeatherForecast, Location
from datetime import datetime, timezone
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError


class LocationFormView(FormView):
    form_class = LocationForm
    template_name = "weather.html"
    success_url = reverse_lazy("forecast")
    forecast_id = 0

    def get_success_url(self):
        return reverse("forecast", kwargs={"id": self.forecast_id})

    def form_valid(self, form):
        data = form.cleaned_data
        # Search Local DB
        forecast = WeatherForecast.objects.filter(
            location__lat=data["lat"], location__long=data["long"]
        ).active()
        if forecast.exists():
            # Send Local DB Data
            weather_data = forecast[0].weather_data
        else:
            # Call Weather API
            weather_data = WeatherAPI(data).openweather()
            # Add Location
            location, created = Location.objects.get_or_create(
                lat=data["lat"], long=data["long"]
            )
            # Add Weather Data
            self.forecast_id = WeatherForecast.objects.create(
                location=location, weather_data=weather_data
            ).id
        return super().form_valid(form)


class WeatherForecastView(TemplateView):
    template_name = "forecast.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["data"] = WeatherForecast.objects.get(id=kwargs["id"])
        except WeatherForecast.DoesNotExist:
            print("Error fetching ID : ", kwargs["id"])
            context["error"] = "Data doesn't exist"
        return context
