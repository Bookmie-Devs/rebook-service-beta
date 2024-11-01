# Generated by Django 4.2.7 on 2024-01-17 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments_app', '0011_rename_reference_paymenthistory_reference_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='paystacksubaccount',
            name='percentage_charge',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
    ]
