from django_seed import Seed    
from shop.models import *
import random
from django.contrib.auth.hashers import make_password
from faker import Faker
import itertools

import os

def run():
    seeder = Seed.seeder()
    
    # Définition des trois possibilités
    roles = ['admin', 'membre', 'webmaster', 'stock']

    # Seed Roles
    seeder.add_entity(
        Roles,
        len(roles),
        {
            'role': lambda x, roles_iter=itertools.cycle(roles): next(roles_iter),
        },
    )
    inserted_pks = seeder.execute()
    print(inserted_pks)

    # Seed Infos site
    seeder.add_entity(InfosQDP, 1, {
        'adresse': 'Wonder Street, USA, New York',
        'email': 'hello@xton.com',
        'telephone': '+01 321 654 214',
        'fax': '+123456789',
        'slogan_site': 'One of the most popular on the web is shopping. Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    })

    inserted_pks = seeder.execute()
    print(inserted_pks)

    # Seed Categories
    categories = [
        'Protéines',
        'Acides Aminés',
        'Vitamines',
        'Compléments',
        'Brûleurs de Graisses',
    ]

    seeder.add_entity(
        Categorie,
        len(categories),
        {
            'nom': lambda x, categories_iter=itertools.cycle(categories): next(categories_iter),
            'promo': lambda x: random.choice([True, False]),
            'pourcentage_promo': lambda x: random.randint(5, 90) if random.choice([True, False]) else None,
        },
    )

    inserted_pks = seeder.execute()
    print(inserted_pks)

    # Seed Users
    users = [
        {
            'username': 'admin',
            'password': make_password('admin123'),
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': Roles.objects.get(id=1),
            'image_banniere_profil': 'bannieres/default-banner.webp',
            'avatar': 'avatars/default-avatar.png',
            'metiers_hobbies': 'Admin',
            'bio': 'Lorem ipsum dolor sit amet',
            'abonne_newsletter': False,
        },
        {
            'username': 'webmaster',
            'password': make_password('webmaster123'),
            'email': 'webmaster@example.com',
            'first_name': 'Webmaster',
            'last_name': 'User',
            'role': Roles.objects.get(id=3),
            'image_banniere_profil': 'bannieres/default-banner.webp',
            'avatar': 'avatars/default-avatar.png',
            'metiers_hobbies': 'Web development',
            'bio': 'Lorem ipsum dolor sit amet',
            'abonne_newsletter': False,
        },
        {
            'username': 'stock',
            'password': make_password('stock123'),
            'email': 'stock@example.com',
            'first_name': 'Stock',
            'last_name': 'User',
            'role': Roles.objects.get(id=4),
            'image_banniere_profil': 'bannieres/default-banner.webp',
            'avatar': 'avatars/default-avatar.png',
            'metiers_hobbies': 'Inventory management',
            'bio': 'Lorem ipsum dolor sit amet',
            'abonne_newsletter': False,
        },
    ]

    for user in users:
        seeder.add_entity(User, 1, user)

    inserted_pks = seeder.execute()
    print(inserted_pks)

    # Seed produits
    seeder.add_entity(Produits, 36, {
        'nom': lambda x: seeder.faker.word(),
        'image_1': lambda x: seeder.faker.image_url(width=670, height=800),
        'image_2': lambda x: seeder.faker.image_url(width=670, height=800),
        'image_3': lambda x: seeder.faker.image_url(width=670, height=800),
        'image_4': lambda x: seeder.faker.image_url(width=670, height=800),
        'image_5': lambda x: seeder.faker.image_url(width=670, height=800),
        'image_6': lambda x: seeder.faker.image_url(width=670, height=800),
        'marque_vendeur': lambda x: random.choice(['MyProtein', 'Prozis', 'HSN', 'Optimum Nutrition', 'MuscleTech', 'Dymatize', 'Cellucor', 'MusclePharm', 'Universal Nutrition']),
        'type': lambda x: random.choice(['gélules', 'poudre']),
        'categorie': lambda x: random.choice(Categorie.objects.all()),
        'quantite_stock': lambda x: random.randint(0, 100),
        'prix': lambda x: random.uniform(10, 100),
        'description': lambda x: seeder.faker.paragraph(),
        'ingredients': lambda x: seeder.faker.text(),
        'macronutriments': lambda x: seeder.faker.text(),
        'variations': lambda x: seeder.faker.word(),
        'en_promo': lambda x: random.choice([True, False]),
        'nature_promo': None,
        'pourcentage_promo': lambda x: random.randint(5, 90) if random.choice([True, False]) else 0,
    })

    inserted_pks = seeder.execute()
    print(inserted_pks)