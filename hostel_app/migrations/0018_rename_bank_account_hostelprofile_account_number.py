# Generated by Django 4.2 on 2023-09-29 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0017_remove_hostelprofile_bank_details_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostelprofile',
            old_name='bank_account',
            new_name='account_number',
        ),
    ]