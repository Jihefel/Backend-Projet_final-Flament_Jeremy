# Generated by Django 4.2.3 on 2023-07-17 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_user_produits_panier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='contacts_echanges',
        ),
    ]
