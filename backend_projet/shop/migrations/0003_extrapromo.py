# Generated by Django 4.2.3 on 2023-07-15 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_user_produits_panier'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraPromo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_promo', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shop.promotions')),
            ],
        ),
    ]