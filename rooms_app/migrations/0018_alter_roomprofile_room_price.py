# Generated by Django 4.2.7 on 2023-12-08 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0017_alter_roomprofile_room_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomprofile',
            name='room_price',
            field=models.DecimalField(decimal_places=7, max_digits=7),
        ),
    ]