# Generated by Django 4.2.7 on 2024-02-10 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_customuser_campus_remove_customuser_college_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpCodeData',
            fields=[
                ('otp_code_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('otp_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='OTP CODE')),
                ('phone', models.CharField(max_length=15, verbose_name='phone number')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('code_life_time', models.DateTimeField(blank=True, null=True, verbose_name='code life time')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'OtpCodeData',
                'verbose_name_plural': 'OtpCodeDatas',
            },
        ),
    ]