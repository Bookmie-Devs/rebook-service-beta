# Generated by Django 4.2.2 on 2023-12-08 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0027_alter_roomprofile_room_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomprofile',
            name='previous_price_check',
        ),
    ]