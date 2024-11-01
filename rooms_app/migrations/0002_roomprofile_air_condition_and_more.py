# Generated by Django 4.2 on 2023-10-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomprofile',
            name='air_condition',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='roomprofile',
            name='contains_bathroom',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='roomprofile',
            name='contains_kitchen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='roomprofile',
            name='floor_no',
            field=models.CharField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='roomprofile',
            name='shared_bathroom',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='roomprofile',
            name='shared_kitchen',
            field=models.BooleanField(default=False),
        ),
    ]
