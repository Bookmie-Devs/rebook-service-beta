# Generated by Django 4.2.7 on 2023-12-03 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0015_roomprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomprofile',
            name='gender',
            field=models.CharField(choices=[('female', 'female'), ('male', 'male')], default='male', max_length=20, verbose_name='Gender of room'),
        ),
    ]