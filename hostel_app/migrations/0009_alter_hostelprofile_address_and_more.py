# Generated by Django 4.2 on 2023-10-30 07:52

from django.db import migrations
import django_google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0008_hostelprofile_geolocation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='address',
            field=django_google_maps.fields.AddressField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='hostelprofile',
            name='geolocation',
            field=django_google_maps.fields.GeoLocationField(blank=True, max_length=100, null=True),
        ),
    ]
