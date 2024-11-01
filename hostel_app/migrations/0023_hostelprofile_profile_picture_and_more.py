# Generated by Django 4.2.7 on 2023-12-05 23:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0022_alter_hostelprofile_hostel_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostelprofile',
            name='profile_picture',
            field=models.ImageField(default='unknown_profile.jpg', upload_to='ManagersProfilePics'),
        ),
        migrations.AlterField(
            model_name='hostelprofile',
            name='hostel_id',
            field=models.UUIDField(default=uuid.UUID('1296fd7a-18b2-47d7-b8c5-962b2257bd98'), editable=False, unique=True),
        ),
    ]
