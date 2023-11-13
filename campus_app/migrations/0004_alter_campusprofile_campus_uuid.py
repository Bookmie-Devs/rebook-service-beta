# Generated by Django 4.2 on 2023-10-23 14:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('campus_app', '0003_alter_campusprofile_campus_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campusprofile',
            name='campus_uuid',
            field=models.UUIDField(default=uuid.UUID('c6ded173-3732-4b7d-91be-fdd16c963401'), editable=False),
        ),
    ]