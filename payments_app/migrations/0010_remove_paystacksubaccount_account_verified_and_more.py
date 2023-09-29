# Generated by Django 4.2 on 2023-09-29 19:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payments_app', '0009_paystacksubaccount_bank_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paystacksubaccount',
            name='account_verified',
        ),
        migrations.RemoveField(
            model_name='paystacksubaccount',
            name='settlement_bank',
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='payment_id',
            field=models.UUIDField(default=uuid.UUID('7d685d5b-56b6-4499-9b0a-f719f9b4757b'), editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='paystacksubaccount',
            name='bank_code',
            field=models.CharField(default='unavailable', max_length=20),
        ),
    ]
