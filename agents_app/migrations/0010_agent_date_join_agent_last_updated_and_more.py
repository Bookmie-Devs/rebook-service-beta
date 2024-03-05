# Generated by Django 4.2.7 on 2024-03-02 19:05

import agents_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents_app', '0009_alter_agent_agent_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='date_join',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='agent',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='agent_code',
            field=models.CharField(default=agents_app.models.genrate_agent_code, editable=False, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]