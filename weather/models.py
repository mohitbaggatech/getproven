from django.db import models
from datetime import datetime, timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from settings import LOCATION_EXPIRY

DETAILING_TYPES = [("C", "Current"), ("M", "Minutely"), ("H", "Hourly"), ("D", "Daily")]


class Location(models.Model):
    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MaxValueValidator(90), MinValueValidator(-90)],
    )
    long = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MaxValueValidator(180), MinValueValidator(-180)],
    )
    created = models.DateTimeField(blank=True, auto_now_add=True)
    updated = models.DateTimeField(blank=True, auto_now=True)

    def __unicode__(self):
        return "%s, %s" % (self.lat, self.long)

    def __str__(self):
        return "%s, %s" % (self.lat, self.long)


class WeatherForecastQuerySet(models.query.QuerySet):
    def active(self):
        expiry_time = datetime.now(timezone.utc) - LOCATION_EXPIRY
        return self.filter(created__gte=expiry_time)


class WeatherForecastManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return WeatherForecastQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        return self.get_queryset().active()


class WeatherForecast(models.Model):
    location = models.ForeignKey(
        Location, null=False, blank=False, on_delete=models.DO_NOTHING
    )
    detailing = models.CharField(max_length=1, choices=DETAILING_TYPES)
    weather_data = models.JSONField()
    created = models.DateTimeField(blank=True, auto_now_add=True)
    updated = models.DateTimeField(blank=True, auto_now=True)

    objects = WeatherForecastManager()

    def __unicode__(self):
        return "%s %s %s" % (self.location, self.detailing, self.created)

    def __str__(self):
        return "%s %s %s" % (self.location, self.detailing, self.created)
