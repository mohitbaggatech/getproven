# Generated by Django 4.2 on 2023-04-12 10:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('long', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailing', models.CharField(choices=[('C', 'Current'), ('M', 'Minute'), ('H', 'Hourly'), ('D', 'Daily')], max_length=1)),
                ('wtime', models.DateTimeField(default=datetime.datetime.now)),
                ('weather_data', models.JSONField()),
            ],
        ),
    ]
