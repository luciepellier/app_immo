# Generated by Django 4.2.3 on 2023-08-10 19:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_immo', '0023_alter_payment_charges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_immo.contract')),
            ],
        ),
    ]