# Generated by Django 4.2.2 on 2023-12-13 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0040_alter_hostelprofile_hostel_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostelprofile',
            old_name='other_phone',
            new_name='other_contact',
        ),
    ]