# Generated by Django 4.2.7 on 2024-02-20 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quick_rooms', '0004_guesthouse_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guesthouseroom',
            name='room_image',
            field=models.ImageField(default='unavailable.jpg', upload_to='GuestHouse'),
        ),
        migrations.AlterField(
            model_name='guesthouseroom',
            name='room_image1',
            field=models.ImageField(default='unavailable.jpg', upload_to='GuestHouse'),
        ),
        migrations.AlterField(
            model_name='guesthouseroom',
            name='room_image2',
            field=models.ImageField(default='unavailable.jpg', upload_to='GuestHouse'),
        ),
        migrations.AlterField(
            model_name='guesthouseroom',
            name='room_image3',
            field=models.ImageField(default='unavailable.jpg', upload_to='GuestHouse'),
        ),
    ]
