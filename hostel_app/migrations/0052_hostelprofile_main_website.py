# Generated by Django 4.2.7 on 2024-02-08 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0051_hostelprofile_no_of_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostelprofile',
            name='main_website',
            field=models.URLField(blank=True, null=True, verbose_name='Main Website'),
        ),
    ]