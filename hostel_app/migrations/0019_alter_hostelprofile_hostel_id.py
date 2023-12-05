# Generated by Django 4.2.7 on 2023-12-04 18:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0018_alter_hostelprofile_hostel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='hostel_id',
            field=models.UUIDField(default=uuid.UUID('3ef49ff6-85f4-4cb1-8944-47a74f6ae71d'), editable=False, unique=True),
        ),
    ]