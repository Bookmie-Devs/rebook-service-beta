# Generated by Django 4.2.7 on 2024-03-01 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_rename_student_id_student_student_id_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_guest_house_manager',
            field=models.BooleanField(default=False, verbose_name='Guest House Manager'),
        ),
    ]
