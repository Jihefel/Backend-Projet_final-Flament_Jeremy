# Generated by Django 4.2.3 on 2023-07-19 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_remove_blogpost_date_modification'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='date_modification',
            field=models.DateField(auto_now=True),
        ),
    ]
