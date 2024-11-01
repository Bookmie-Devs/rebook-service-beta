# Generated by Django 4.2.7 on 2024-01-21 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0045_hostelprofile_room_image2_hostelprofile_room_image3'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostelprofile',
            name='hostel_image2',
            field=models.ImageField(default='unavailable.jpg', upload_to='HostelProfiles'),
        ),
        migrations.AddField(
            model_name='hostelprofile',
            name='hostel_image3',
            field=models.ImageField(default='unavailable.jpg', upload_to='HostelProfiles'),
        ),
        migrations.AddField(
            model_name='hostelprofile',
            name='hostel_image4',
            field=models.ImageField(default='unavailable.jpg', upload_to='HostelProfiles'),
        ),
        migrations.AddField(
            model_name='hostelprofile',
            name='hostel_image5',
            field=models.ImageField(default='unavailable.jpg', upload_to='HostelProfiles'),
        ),
        migrations.AddField(
            model_name='hostelprofile',
            name='room_image4',
            field=models.ImageField(default='unavailable.jpg', upload_to='RoomImages', verbose_name='Image4 of one room'),
        ),
        migrations.AddField(
            model_name='hostelprofile',
            name='room_image5',
            field=models.ImageField(default='unavailable.jpg', upload_to='RoomImages', verbose_name='Image5 of one room'),
        ),
        migrations.AddField(
            model_name='hostelprofile',
            name='room_image6',
            field=models.ImageField(default='unavailable.jpg', upload_to='RoomImages', verbose_name='Image6 of one room'),
        ),
    ]
