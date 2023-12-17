# Generated by Django 4.2.7 on 2023-12-16 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campus_guest_house', '0002_rename_guest_hosue_name_guesthouse_guest_house_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='guesthouse',
            name='house_code',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='guesthouse',
            name='house_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='guesthouse',
            name='house_image',
            field=models.ImageField(default='unavailable.jpg', upload_to='GuestHouseImage'),
        ),
        migrations.AddField(
            model_name='guesthouse',
            name='manager',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='guesthouse',
            name='account_number',
            field=models.CharField(default='unavailable', help_text='Can also be a mobile money account', max_length=70),
        ),
    ]
