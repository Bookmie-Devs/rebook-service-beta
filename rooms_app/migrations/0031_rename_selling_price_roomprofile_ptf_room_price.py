# Generated by Django 4.2.2 on 2023-12-09 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0030_roomprofile_selling_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomprofile',
            old_name='selling_price',
            new_name='ptf_room_price',
        ),
    ]
