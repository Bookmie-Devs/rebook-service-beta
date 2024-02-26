# Generated by Django 4.2.7 on 2024-02-20 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quick_rooms', '0011_guesthouseroom_ptf_room_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='guesthouseroom',
            name='previous_price_check',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=7, null=True),
        ),
    ]
