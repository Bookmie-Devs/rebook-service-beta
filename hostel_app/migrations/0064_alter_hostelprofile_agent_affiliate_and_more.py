# Generated by Django 4.2.7 on 2024-03-02 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents_app', '0006_remove_hostelagent_campus_affiliation_and_more'),
        ('hostel_app', '0063_alter_hostelprofile_no_of_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostelprofile',
            name='agent_affiliate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='agents_app.agent'),
        ),
        migrations.AlterField(
            model_name='hostelprofile',
            name='no_of_likes',
            field=models.IntegerField(default=35, verbose_name='Likes'),
        ),
    ]
