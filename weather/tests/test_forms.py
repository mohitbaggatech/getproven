from django.test import TestCase
from weather.models import Location
from weather.forms import LocationForm


class LocationFormTest(TestCase):
    def test_valid_form(self):
        l = Location.objects.create(lat=-21.234, long=+143.123)
        data = {"lat": l.lat, "long": l.long, "detailing": "C"}
        form = LocationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        l = Location.objects.create(lat=-21.234, long=+143.123)
        data = {"lat": l.lat, "long": l.long, "detailing": "K"}
        form = LocationForm(data=data)
        self.assertFalse(form.is_valid())
