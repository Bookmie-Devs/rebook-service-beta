# Generated by Django 4.2 on 2023-09-26 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0014_rename_on_map_location_hostelprofile_map_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='location',
            field=models.CharField(default='location unavailable', max_length=500),
        ),
    ]
