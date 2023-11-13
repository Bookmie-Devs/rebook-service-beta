# Generated by Django 4.2 on 2023-10-28 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews_app', '0003_customercare'),
    ]

    operations = [
        migrations.AddField(
            model_name='customercare',
            name='issue_resolved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feedbackmessage',
            name='issue_resolved',
            field=models.BooleanField(default=False),
        ),
    ]