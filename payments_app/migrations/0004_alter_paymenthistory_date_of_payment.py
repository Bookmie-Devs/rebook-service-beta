# Generated by Django 4.2 on 2023-10-11 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments_app', '0003_paymenthistory_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='date_of_payment',
            field=models.DateField(auto_now_add=True),
        ),
    ]
