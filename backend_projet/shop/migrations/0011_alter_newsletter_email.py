# Generated by Django 4.2.3 on 2023-07-18 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_user_avatar_alter_user_image_banniere_profil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
