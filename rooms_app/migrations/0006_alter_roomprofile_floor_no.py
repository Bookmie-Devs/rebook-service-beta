# Generated by Django 4.2 on 2023-10-11 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0005_roomprofile_contains_toilet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomprofile',
            name='floor_no',
            field=models.IntegerField(default=0, verbose_name='Floor number'),
        ),
    ]
