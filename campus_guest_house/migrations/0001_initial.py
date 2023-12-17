# Generated by Django 4.2.7 on 2023-12-16 20:44

from django.db import migrations, models
import django.db.models.deletion
import django_google_maps.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campus_app', '0014_campusprofile_alias_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_hosue_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=13, verbose_name='Guess House Number')),
                ('account_number', models.CharField(default='unavailable', max_length=70)),
                ('bank_code', models.CharField(choices=[('280100', 'Access Bank'), ('080100', 'ADB Bank Limited'), ('030100', 'Absa Bank Ghana Ltd'), ('MTN', 'MTN'), ('VOD', 'Vodafone'), ('ATL', 'AirtelTigo'), ('070101', 'ARB Apex Bank'), ('210100', 'Bank of Africa Ghana'), ('010100', 'Bank of Ghana'), ('300335', 'Best Point Savings and Loans'), ('140100', 'CAL Bank Limited'), ('340100', 'Consolidated Bank Ghana Limited'), ('130100', 'Ecobank Ghana Limited'), ('200100', 'FBNBank Ghana Limited'), ('240100', 'Fidelity Bank Ghana Limited'), ('170100', 'First Atlantic Bank Limited'), ('330100', 'First National Bank Ghana Limited'), ('040100', 'GCB Bank Limited'), ('230100', 'Guaranty Trust Bank (Ghana) Limited'), ('050100', 'National Investment Bank Limited'), ('360100', 'OmniBSCI Bank'), ('180100', 'Prudential Bank Limited'), ('110100', 'Republic Bank (GH) Limited'), ('300361', 'Services Integrity Savings and Loans'), ('090100', 'Société Générale Ghana Limited'), ('190100', 'Stanbic Bank Ghana Limited'), ('020100', 'Standard Chartered Bank Ghana Limited'), ('060100', 'United Bank for Africa Ghana Limited'), ('100100', 'Universal Merchant Bank Ghana Limited'), ('120100', 'Zenith Bank Ghana')], default='unavailable', max_length=50)),
                ('mobile_money', models.CharField(default='unavailable', max_length=14)),
                ('manager_contact', models.CharField(blank=True, max_length=10, verbose_name="Manager's Contact")),
                ('address', django_google_maps.fields.AddressField(blank=True, max_length=200, null=True)),
                ('geolocation', django_google_maps.fields.GeoLocationField(blank=True, max_length=100, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='campus_app.campusprofile')),
            ],
            options={
                'verbose_name': 'GuestHouse',
                'verbose_name_plural': 'GuestHouses',
            },
        ),
    ]