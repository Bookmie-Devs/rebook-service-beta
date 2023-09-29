# Generated by Django 4.2 on 2023-09-29 19:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payments_app', '0011_paystacksubaccount_account_verified_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymenthistory',
            name='id',
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='payment_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
