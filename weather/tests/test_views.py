from django.test import RequestFactory, TestCase
from weather.views import WeatherForecastView
from weather.models import Location, WeatherForecast
from django.urls import reverse
from urllib.parse import urlencode


class WeatherForecastViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.location = Location.objects.create(lat=-89.981, long=+123.125)
        self.forecast = WeatherForecast.objects.create(
            location=self.location, detailing="C", weather_data={"dummy": True}
        )

    def test_context_data(self):
        request = RequestFactory().get("/forecast/{id}".format(id=self.forecast.id))
        view = WeatherForecastView()
        view.setup(request)

        context = view.get_context_data(id=self.forecast.id)
        self.assertIn("data", context)

    def test_invalid_data(self):
        request = RequestFactory().get("/forecast/{id}".format(id=-1))
        view = WeatherForecastView()
        view.setup(request)

        context = view.get_context_data(id=-1)
        self.assertIn("error", context)


class LocationFormViewTest(TestCase):
    @classmethod
    def setUp(self):
        self.location = Location.objects.create(lat=-89.981, long=+123.125)
        self.forecast = WeatherForecast.objects.create(
            location=self.location, detailing="C", weather_data={"dummy": True}
        )

    def test_redirect_url(self):
        response = self.client.post(
            reverse("weather"),
            urlencode({"lat": -89.981, "long": +123.125, "detailing": "C"}),
            content_type="application/x-www-form-urlencoded",
        )
        # Check Redirect
        self.assertEqual(response.status_code, 302)

    def test_new_data(self):
        response = self.client.post(
            reverse("weather"),
            urlencode({"lat": -10.01, "long": +90.123, "detailing": "C"}),
            content_type="application/x-www-form-urlencoded",
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
