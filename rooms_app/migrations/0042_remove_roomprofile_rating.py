# Generated by Django 4.2.7 on 2024-02-28 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0041_roomprofile_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomprofile',
            name='rating',
        ),
    ]
