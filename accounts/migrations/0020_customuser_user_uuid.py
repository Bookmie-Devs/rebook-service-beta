# Generated by Django 4.2.7 on 2024-04-01 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_rename_is_hostel_agent_customuser_is_bookmie_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_uuid',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
    ]
