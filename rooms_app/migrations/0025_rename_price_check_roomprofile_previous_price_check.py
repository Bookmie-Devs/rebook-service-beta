# Generated by Django 4.2.2 on 2023-12-08 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0024_alter_roomprofile_price_check'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomprofile',
            old_name='price_check',
            new_name='previous_price_check',
        ),
    ]
