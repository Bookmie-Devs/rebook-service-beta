# Generated by Django 4.2.7 on 2024-03-02 18:55

import agents_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents_app', '0007_delete_hostelagent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='agent_code_generated',
        ),
        migrations.AlterField(
            model_name='agent',
            name='agent_code',
            field=models.CharField(default=agents_app.models.genrate_agent_code, editable=False, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]
