from django.test import TestCase
from weather.models import Location, WeatherForecast


class LocationTest(TestCase):
    def create_location(self, lat=-89.981, long=+123.125):
        return Location.objects.create(lat=lat, long=long)

    def test_location_creation(self):
        l = self.create_location()
        self.assertTrue(isinstance(l, Location))
        self.assertEqual(l.__unicode__(), "%s, %s" % (l.lat, l.long))
        self.assertEqual(l.__str__(), "%s, %s" % (l.lat, l.long))


class WeatherForecastTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.location = Location.objects.create(lat=-89.981, long=+123.125)

    def create_forecast(self, detailing="C", weather_data={"dummy": True}):
        return WeatherForecast.objects.create(
            location=self.location, detailing=detailing, weather_data=weather_data
        )

    def test_forecast_creation(self):
        f = self.create_forecast()
        self.assertTrue(isinstance(f, WeatherForecast))
        self.assertEqual(f.detailing, "C")
        self.assertEqual(f.weather_data, {"dummy": True})
        self.assertEqual(
            f.__unicode__(), "%s %s %s" % (f.location, f.detailing, f.created)
        )
        self.assertEqual(f.__str__(), "%s %s %s" % (f.location, f.detailing, f.created))
