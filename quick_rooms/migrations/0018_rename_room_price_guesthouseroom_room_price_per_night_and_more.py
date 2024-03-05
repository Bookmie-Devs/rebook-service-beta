# Generated by Django 4.2.7 on 2024-03-01 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quick_rooms', '0017_alter_paystackguesthousesubaccount_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guesthouseroom',
            old_name='room_price',
            new_name='room_price_per_night',
        ),
        migrations.RemoveField(
            model_name='guestbooking',
            name='campus',
        ),
        migrations.RemoveField(
            model_name='guesthousemanager',
            name='campus_affiliation',
        ),
        migrations.AddField(
            model_name='guesthouseroom',
            name='room_number',
            field=models.CharField(default='unavailable', max_length=50),
        ),
        migrations.AlterField(
            model_name='guesthouse',
            name='manager',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quick_rooms.guesthousemanager'),
        ),
    ]