# Generated by Django 4.2.7 on 2024-02-05 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments_app', '0019_paymenthistory_is_half_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='completed_full_payment',
            field=models.BooleanField(default=False),
        ),
    ]
