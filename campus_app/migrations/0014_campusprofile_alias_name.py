# Generated by Django 4.2.2 on 2023-12-11 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus_app', '0013_collegeprofile_delete_collegesprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='campusprofile',
            name='alias_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]