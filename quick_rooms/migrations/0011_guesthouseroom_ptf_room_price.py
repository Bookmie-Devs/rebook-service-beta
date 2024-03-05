# Generated by Django 4.2.7 on 2024-02-20 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quick_rooms', '0010_rename_reference_guestpaymenthistory_reference_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guesthouseroom',
            name='ptf_room_price',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=8),
        ),
    ]