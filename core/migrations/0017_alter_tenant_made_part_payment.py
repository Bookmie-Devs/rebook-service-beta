# Generated by Django 4.2.7 on 2024-02-05 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_tenant_amount_left_to_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='made_part_payment',
            field=models.BooleanField(default=False, verbose_name='MADE PART PAYMENT'),
        ),
    ]
