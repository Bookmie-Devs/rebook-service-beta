# Generated by Django 4.2.7 on 2024-03-01 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quick_rooms', '0018_rename_room_price_guesthouseroom_room_price_per_night_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guesthouseroom',
            old_name='room_image1',
            new_name='room_image4',
        ),
    ]