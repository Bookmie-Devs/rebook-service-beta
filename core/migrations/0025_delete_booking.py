# Generated by Django 4.2.7 on 2024-02-23 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_booking_campus_remove_booking_room_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Booking',
        ),
    ]