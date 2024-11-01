# Generated by Django 4.2.7 on 2023-12-05 22:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0019_alter_hostelprofile_hostel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='hostel_id',
            field=models.UUIDField(default=uuid.UUID('fca0c78b-a458-4011-b2a3-f8be599c281b'), editable=False, unique=True),
        ),
    ]
