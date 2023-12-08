# Generated by Django 4.2.2 on 2023-12-08 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0023_roomprofile_price_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomprofile',
            name='price_check',
            field=models.DecimalField(blank=True, decimal_places=1, editable=False, max_digits=7, null=True),
        ),
    ]
