# Generated by Django 4.2.7 on 2024-02-08 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0037_roomprofile_accept_half_payment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomprofile',
            name='no_of_likes',
            field=models.IntegerField(default=1, verbose_name='Likes'),
        ),
    ]