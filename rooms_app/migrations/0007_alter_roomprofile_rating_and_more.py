# Generated by Django 4.2 on 2023-09-25 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_app', '0006_alter_roomprofile_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomprofile',
            name='rating',
            field=models.CharField(choices=[('⭐⭐⭐⭐', '⭐⭐⭐⭐'), ('⭐⭐⭐', '⭐⭐⭐'), ('⭐⭐', '⭐⭐'), ('⭐', '⭐')], default='⭐', max_length=15),
        ),
        migrations.AlterField(
            model_name='roomprofile',
            name='room_capacity',
            field=models.PositiveIntegerField(default=4),
        ),
    ]
