# Generated by Django 4.2.3 on 2023-08-25 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_immo', '0030_alter_contract_agency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='deposit',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='rental',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
