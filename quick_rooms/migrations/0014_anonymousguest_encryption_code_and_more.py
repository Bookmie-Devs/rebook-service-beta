# Generated by Django 4.2.7 on 2024-02-23 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quick_rooms', '0013_alter_guestpaymenthistory_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymousguest',
            name='encryption_code',
            field=models.CharField(blank=True, editable=False, max_length=10, null=True, verbose_name='anonymous encryption'),
        ),
        migrations.AlterField(
            model_name='anonymousguest',
            name='quest_code',
            field=models.CharField(blank=True, editable=False, max_length=10, null=True, verbose_name='anonymous code'),
        ),
    ]