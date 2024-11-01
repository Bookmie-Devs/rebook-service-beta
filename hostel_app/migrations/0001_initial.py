# Generated by Django 4.2 on 2023-10-07 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campus_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HostelProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostel_name', models.CharField(max_length=50)),
                ('hostel_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('hostel_code', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('hostel_image', models.ImageField(default='unavailable.jpg', upload_to='HostelProfiles')),
                ('category', models.CharField(choices=[('Hostel', 'Hostel'), ('Homestel', 'Homestel'), ('Apartment', 'Apartment')], default='Hostel', max_length=15, verbose_name='type')),
                ('rating', models.IntegerField(choices=[(4, '⭐⭐⭐⭐'), (3, '⭐⭐⭐'), (2, '⭐⭐'), (1, '⭐')], default='⭐', verbose_name='Stars')),
                ('price_range', models.CharField(blank=True, default='unavailable', max_length=50)),
                ('hostel_motto', models.CharField(blank=True, max_length=2000)),
                ('number_of_rooms', models.IntegerField(default=5)),
                ('hostel_email', models.EmailField(blank=True, max_length=254)),
                ('account_number', models.CharField(default='unavailable', max_length=50)),
                ('bank_code', models.CharField(default='unavailable', max_length=50)),
                ('mobile_money', models.CharField(default='unavailable', max_length=14)),
                ('managers_contact', models.CharField(blank=True, max_length=10)),
                ('contact', models.CharField(max_length=10)),
                ('location', models.CharField(default='location unavailable', max_length=500)),
                ('other_phone', models.CharField(blank=True, max_length=10)),
                ('map_location', models.CharField(default='unavailable', max_length=10000)),
                ('main_website', models.URLField(blank=True, null=True, verbose_name='Hostel Website')),
                ('address', models.CharField(max_length=255)),
                ('verified', models.BooleanField(default=False)),
                ('occupied', models.BooleanField(default=False)),
                ('campus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='campus_app.campusprofile')),
                ('hostel_manager', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hostels', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hostel_profiles',
                'ordering': ('-hostel_name',),
            },
        ),
    ]
