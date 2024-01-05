# Generated by Django 4.2.7 on 2024-01-05 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hostel_app', '0044_alter_hostelprofile_hostel_manager_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date recorded')),
                ('last_updated', models.DateField(auto_now=True, verbose_name='last updated')),
                ('year', models.PositiveIntegerField(default=2024)),
                ('amount_made', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hostel_app.hostelprofile')),
            ],
        ),
    ]
