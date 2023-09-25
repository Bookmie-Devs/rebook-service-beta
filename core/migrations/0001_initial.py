# Generated by Django 4.2 on 2023-09-23 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms_app', '0001_initial'),
        ('campus_app', '0001_initial'),
        ('hostel_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('room_number', models.CharField(max_length=20)),
                ('student_id', models.CharField(max_length=20)),
                ('booking_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campus_app.campusprofile')),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel_app.hostelprofile')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms_app.roomprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-start_time',),
            },
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('tenant_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('payed', models.BooleanField(default=False)),
                ('checked_in', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.booking')),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostel_app.hostelprofile')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms_app.roomprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-start_date',),
            },
        ),
    ]
