# Generated by Django 4.2.2 on 2023-11-29 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus_app', '0010_campusprofile_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campusprofile',
            name='location',
            field=models.CharField(max_length=255, null=True),
        ),
    ]