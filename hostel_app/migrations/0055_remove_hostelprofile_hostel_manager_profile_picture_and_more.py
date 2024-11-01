# Generated by Django 4.2.7 on 2024-03-01 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hostel_app', '0054_alter_hostelprofile_no_of_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostelprofile',
            name='hostel_manager_profile_picture',
        ),
        migrations.RemoveField(
            model_name='hostelprofile',
            name='rating',
        ),
        migrations.AlterField(
            model_name='hostelprofile',
            name='hostel_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='hostelprofile',
            name='hostel_manager',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hostels', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hostelprofile',
            name='no_of_likes',
            field=models.IntegerField(default=22, verbose_name='Likes'),
        ),
    ]
