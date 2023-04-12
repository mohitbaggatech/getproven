from django.shortcuts import render
from weather.forms import LocationForm
from django.views import View
from django.http import HttpResponseRedirect
from weather.cloud_third_party import WeatherAPI
from weather.models import WeatherForecast, Location
from datetime import datetime, timezone

class LocationFormView(View):
    form_class = LocationForm
    initial = {"appid": "fbb5de0cf2526f0ba2ea28a2f47ef82d"}
    template_name = "weather.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Search Local DB
            forecast = WeatherForecast.objects.filter(location__lat=data['lat'], location__long=data['long'])
            fetch_data = False
            location = None
            if len(forecast):
                # Check 10 minute window (DATA EXPIRY)
                if (datetime.now(timezone.utc) - forecast[0].created).total_seconds() / 60 <= 10:
                    # Send Local DB Data
                    weather_data = forecast[0].weather_data
                else:
                    # Get Data
                    fetch_data = True
                    location = forecast[0].location
            else:
                # Get Data
                fetch_data = True
            if fetch_data:
                # Call Weather API
                weather_data = WeatherAPI(data).fetch_data()
                if isinstance(weather_data, dict) and 'error' in weather_data:
                    # Error Fetching Data
                    return render(request, self.template_name, {"form": form, "error" : weather_data['error']})
                if not location:
                    # Add Location
                    location = Location.objects.create(lat = data['lat'], long=data['long'])
                # Add Weather Data
                WeatherForecast.objects.create(location = location, weather_data = weather_data)
            # <process form cleaned data>
            return render(request, self.template_name, {"form": form, "weather_data": weather_data})
        return render(request, self.template_name, {"form": form})
