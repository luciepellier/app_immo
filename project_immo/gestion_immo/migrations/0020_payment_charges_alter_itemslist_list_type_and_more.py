# Generated by Django 4.2.3 on 2023-08-10 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_immo', '0019_remove_contract_deposit_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='charges',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='itemslist',
            name='list_type',
            field=models.CharField(choices=[('Entrée', 'Entrée'), ('Sortie', 'Sortie')], default='Entrée', max_length=6),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
