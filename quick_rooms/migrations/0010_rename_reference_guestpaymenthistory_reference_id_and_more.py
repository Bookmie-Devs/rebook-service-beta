# Generated by Django 4.2.7 on 2024-02-20 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quick_rooms', '0009_remove_guestbooking_room_number_guesthouse_campus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guestpaymenthistory',
            old_name='reference',
            new_name='reference_id',
        ),
        migrations.RemoveField(
            model_name='guestpaymenthistory',
            name='guest_user',
        ),
        migrations.RemoveField(
            model_name='guestpaymenthistory',
            name='hostel',
        ),
        migrations.RemoveField(
            model_name='guestpaymenthistory',
            name='room',
        ),
        migrations.AddField(
            model_name='guestpaymenthistory',
            name='booking',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='quick_rooms.guestbooking'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='guestpaymenthistory',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='guestpaymenthistory',
            name='email',
            field=models.EmailField(default='bookmie.com@gmail.com', max_length=254),
        ),
        migrations.CreateModel(
            name='PaystackGuestHouseSubAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bussiness_name', models.CharField(max_length=50)),
                ('account_number', models.CharField(max_length=50)),
                ('subaccount_code', models.CharField(default='unavailable', max_length=50, unique=True)),
                ('primary_contact_name', models.CharField(default='unavailable', max_length=30)),
                ('bank_code', models.CharField(default='unavailable', max_length=50)),
                ('settlement_bank', models.CharField(default='unavailable', max_length=80)),
                ('percentage_charge', models.DecimalField(decimal_places=3, default=0, max_digits=5, verbose_name='percentage charge %')),
                ('account_verified', models.BooleanField(default=False)),
                ('is_updating_subaccount', models.BooleanField(default=False)),
                ('update_message', models.CharField(blank=True, max_length=30, null=True)),
                ('guest_house', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quick_rooms.guesthouse')),
            ],
            options={
                'db_table': 'paystack_guesthouse_sub_accounts',
            },
        ),
    ]
