# Generated by Django 4.2.7 on 2024-02-18 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents_app', '0004_alter_hostelagent_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date recorded')),
                ('last_updated', models.DateField(auto_now=True, verbose_name='last updated')),
                ('year', models.PositiveIntegerField(default=2024)),
                ('amount_made', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents_app.hostelagent')),
            ],
        ),
    ]
