# Generated by Django 4.2.7 on 2024-02-20 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_hostel_worker',
            field=models.BooleanField(default=False, verbose_name='Hostel Woker/Portar'),
        ),
    ]
