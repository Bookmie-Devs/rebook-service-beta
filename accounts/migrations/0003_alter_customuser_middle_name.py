# Generated by Django 4.2 on 2023-11-03 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_is_hostel_worker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='middle_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
