# Generated by Django 4.2 on 2023-10-26 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedbackmessage',
            old_name='data_sent',
            new_name='date_sent',
        ),
    ]