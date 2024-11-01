# Generated by Django 4.2.2 on 2023-12-08 22:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0038_alter_hostelprofile_hostel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='hostel_id',
            field=models.UUIDField(default=uuid.UUID('9ec4ea39-a304-4285-bb09-e2bde9832780'), editable=False, unique=True),
        ),
    ]
