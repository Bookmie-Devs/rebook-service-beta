# Generated by Django 4.2.7 on 2024-02-23 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_tenant_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='campus',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='room_number',
        ),
    ]
