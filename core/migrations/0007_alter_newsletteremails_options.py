# Generated by Django 4.2 on 2023-11-03 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_generalnewsletter_newslettermessage_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletteremails',
            options={'verbose_name': 'News letter Emails', 'verbose_name_plural': 'News letters Emails'},
        ),
    ]
