# Generated by Django 4.2.2 on 2023-12-09 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0031_rename_selling_price_roomprofile_ptf_room_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomprofile',
            name='ptf_room_price',
            field=models.DecimalField(decimal_places=1, default=0.0, editable=False, max_digits=8),
        ),
    ]
