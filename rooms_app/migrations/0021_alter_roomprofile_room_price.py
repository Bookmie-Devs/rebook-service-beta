# Generated by Django 4.2.7 on 2023-12-08 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0020_alter_roomprofile_room_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomprofile',
            name='room_price',
            field=models.FloatField(max_length=1),
        ),
    ]
