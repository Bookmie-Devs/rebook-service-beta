# Generated by Django 4.2.7 on 2024-02-19 14:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quick_rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestHouseRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('room_image', models.ImageField(upload_to='GuestHouse')),
                ('room_image1', models.ImageField(upload_to='GuestHouse')),
                ('room_image2', models.ImageField(upload_to='GuestHouse')),
                ('room_image3', models.ImageField(upload_to='GuestHouse')),
                ('room_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('occupied', models.BooleanField(default=False)),
                ('quest_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quick_rooms.guesthouse')),
            ],
            options={
                'verbose_name': 'GuestHouseRoom',
                'verbose_name_plural': 'GuestHouseRooms',
            },
        ),
        migrations.AlterField(
            model_name='guestbooking',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quick_rooms.guesthouseroom'),
        ),
        migrations.AlterField(
            model_name='guestpaymenthistory',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quick_rooms.guesthouseroom'),
        ),
        migrations.DeleteModel(
            name='GuestHouseRooms',
        ),
    ]