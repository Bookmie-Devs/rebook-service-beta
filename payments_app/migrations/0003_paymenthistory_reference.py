# Generated by Django 4.2 on 2023-10-10 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments_app', '0002_alter_paystacksubaccount_subaccount_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='reference',
            field=models.CharField(default='unavailable', editable=False, max_length=500, unique=True),
        ),
    ]