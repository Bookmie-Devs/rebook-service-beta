# Generated by Django 4.2.7 on 2024-03-03 12:59

from django.db import migrations, models
import hostel_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0071_remove_hostelprofile_hostel_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostelprofile',
            name='hostel_router_id',
            field=models.CharField(default=hostel_app.models.genrate_hostel_code, max_length=10, null=True),
        ),
    ]