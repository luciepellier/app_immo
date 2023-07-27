# Generated by Django 4.2.3 on 2023-07-27 14:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_immo', '0009_alter_contract_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='occupant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_immo.occupant'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
