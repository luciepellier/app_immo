# Generated by Django 4.2.3 on 2023-07-27 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_immo', '0012_alter_contract_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemslist',
            name='list_type',
            field=models.CharField(choices=[('Entrée', "D'entrée"), ('Sortie', 'De sortie')], default='Entrée', max_length=6),
        ),
    ]
