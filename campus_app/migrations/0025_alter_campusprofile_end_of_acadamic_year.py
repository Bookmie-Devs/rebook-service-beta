# Generated by Django 4.2.7 on 2024-01-30 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus_app', '0024_alter_campusprofile_end_of_acadamic_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campusprofile',
            name='end_of_acadamic_year',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]