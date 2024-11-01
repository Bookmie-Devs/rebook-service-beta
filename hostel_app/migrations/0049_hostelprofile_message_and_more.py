# Generated by Django 4.2.7 on 2024-02-07 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0048_hostelprofile_agent_affiliate'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostelprofile',
            name='message',
            field=models.TextField(default='unavailable'),
        ),
        migrations.AddField(
            model_name='hostelprofile',
            name='send_management_sms',
            field=models.BooleanField(default=False),
        ),
    ]
