# Generated by Django 4.2.2 on 2023-12-02 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0013_remove_hostelprofile_map_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostelprofile',
            name='room_image',
            field=models.ImageField(default='unavailable.jpg', upload_to='RoomImages'),
        ),
    ]
