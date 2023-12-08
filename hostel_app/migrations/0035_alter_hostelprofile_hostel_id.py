# Generated by Django 4.2.2 on 2023-12-08 19:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0034_alter_hostelprofile_hostel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='hostel_id',
            field=models.UUIDField(default=uuid.UUID('6a187ae9-c63c-45c4-9484-36b02895b251'), editable=False, unique=True),
        ),
    ]
