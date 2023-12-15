# Generated by Django 4.2.7 on 2023-12-11 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0032_alter_roomprofile_ptf_room_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomprofile',
            name='booking_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='roomprofile',
            name='platform_occupied',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='roomprofile',
            name='previous_price_check',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='roomprofile',
            name='ptf_room_price',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=8),
        ),
        migrations.AlterField(
            model_name='roomprofile',
            name='room_price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]