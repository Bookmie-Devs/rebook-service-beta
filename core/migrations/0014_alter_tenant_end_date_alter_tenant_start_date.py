# Generated by Django 4.2.7 on 2024-01-30 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_tenant_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
