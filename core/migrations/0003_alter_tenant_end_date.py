# Generated by Django 4.2 on 2023-10-19 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_tenant_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='end_date',
            field=models.DateTimeField(editable=False),
        ),
    ]
