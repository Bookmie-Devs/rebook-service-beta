# Generated by Django 4.2.7 on 2024-03-02 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0066_alter_hostelprofile_no_of_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='no_of_likes',
            field=models.IntegerField(default=20, verbose_name='Likes'),
        ),
    ]