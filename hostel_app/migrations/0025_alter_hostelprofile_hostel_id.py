# Generated by Django 4.2.2 on 2023-12-07 12:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0024_rename_profile_picture_hostelprofile_hostel_manager_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='hostel_id',
            field=models.UUIDField(default=uuid.UUID('924292a7-a11a-4a0a-a6b5-7dc9c1b6885e'), editable=False, unique=True),
        ),
    ]
