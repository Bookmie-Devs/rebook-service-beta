# Generated by Django 4.2.7 on 2024-01-30 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_tenant_end_date_alter_tenant_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='room_number',
            field=models.CharField(default=0, max_length=10, verbose_name='Room number'),
        ),
    ]
