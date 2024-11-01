# Generated by Django 4.2.2 on 2023-12-02 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0014_hostelprofile_room_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='room_image',
            field=models.ImageField(default='unavailable.jpg', upload_to='RoomImages', verbose_name='Image of one room'),
        ),
    ]
