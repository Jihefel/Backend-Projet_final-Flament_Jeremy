# Generated by Django 4.2.3 on 2023-07-18 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_produitscommandes_quantite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandes',
            name='prix_total',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
    ]
