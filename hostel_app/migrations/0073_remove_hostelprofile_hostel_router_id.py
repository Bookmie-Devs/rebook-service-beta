# Generated by Django 4.2.7 on 2024-03-03 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0072_hostelprofile_hostel_router_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostelprofile',
            name='hostel_router_id',
        ),
    ]