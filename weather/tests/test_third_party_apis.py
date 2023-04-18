from django.test import TestCase
from weather.models import DETAILING_TYPES
from weather.cloud_third_party import WeatherAPI


class WeatherAPITests(TestCase):
    def test_api(self, data={"lat": +10.123, "long": -10.123}):
        for detail in DETAILING_TYPES:
            response = WeatherAPI(dict(detailing=detail, **data)).openweather()
            self.assertNotEqual(response, {})

    def test_invalid_input(
        self, data={"lat": +10.123, "long": -190.123, "detailing": "C"}
    ):
        response = WeatherAPI(data).openweather()
        self.assertEqual(response, {})
