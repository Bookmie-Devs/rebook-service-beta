# Generated by Django 4.2 on 2023-10-09 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0003_alter_hostelprofile_account_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='account_number',
            field=models.CharField(default='unavailable', max_length=70),
        ),
    ]
