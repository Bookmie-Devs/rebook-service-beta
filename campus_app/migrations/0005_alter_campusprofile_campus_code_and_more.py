# Generated by Django 4.2 on 2023-10-23 14:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('campus_app', '0004_alter_campusprofile_campus_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campusprofile',
            name='campus_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='campusprofile',
            name='campus_uuid',
            field=models.UUIDField(default=uuid.UUID('4ad4496d-d0f0-40fe-bb4e-0e93aeb5dc5a'), editable=False),
        ),
    ]