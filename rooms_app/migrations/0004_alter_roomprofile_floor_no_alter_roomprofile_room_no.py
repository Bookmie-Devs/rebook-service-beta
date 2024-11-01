# Generated by Django 4.2 on 2023-10-10 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0003_remove_roomprofile_shared_bathroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomprofile',
            name='floor_no',
            field=models.CharField(default=0, max_length=20, verbose_name='Floor number'),
        ),
        migrations.AlterField(
            model_name='roomprofile',
            name='room_no',
            field=models.CharField(default=0, max_length=20, verbose_name='Room number'),
        ),
    ]
