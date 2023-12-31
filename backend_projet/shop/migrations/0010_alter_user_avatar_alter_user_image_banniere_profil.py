# Generated by Django 4.2.3 on 2023-07-18 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_user_avatar_alter_user_image_banniere_profil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default-avatar.png', upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image_banniere_profil',
            field=models.ImageField(blank=True, default='bannieres/default-banner.webp', upload_to='bannieres/'),
        ),
    ]
