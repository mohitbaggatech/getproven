# Generated by Django 4.2 on 2023-04-12 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_location_created_location_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='weatherforecast',
            name='location',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='weather.location'),
            preserve_default=False,
        ),
    ]
