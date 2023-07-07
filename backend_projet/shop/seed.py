from django_seed import Seed    
from shop.models import *
import random
from django.contrib.auth.hashers import make_password
from faker import Faker
from django.contrib.auth.models import User, Group, Permission
import itertools

import os

def run():
    seeder = Seed.seeder()
    
    # Définition des trois possibilités
    roles = ['admin', 'membre', 'webmaster']

    # Seed Group
    group_pks = seeder.add_entity(
        Group,
        len(roles),
        {
            'name': lambda x, roles_iter=itertools.cycle(roles): next(roles_iter),
        },
    )


    # Seed Categorie
    seeder.add_entity(
        Categorie,
        5,
        {
            'nom': lambda x: seeder.faker.word(),
            'promo': lambda x: seeder.faker.boolean(),
            'pourcentage_promo': lambda x: seeder.faker.random_int(min=0, max=100),
        },
    )

    # Seed Promotions
    seeder.add_entity(
        Promotions,
        5,
        {
            'nom': lambda x: seeder.faker.name(),
            'pourcentage_promo': lambda x: seeder.faker.random_int(min=0, max=100)*5,
            'slogan': lambda x: seeder.faker.sentence(),
            'description': lambda x: seeder.faker.paragraph(),
            'image_illustration': 'promotions/image.jpg',
            'date_debut': lambda x: seeder.faker.date_this_year(),
            'date_fin': lambda x: seeder.faker.date_this_year(),
        },
    )

    # Seed Produits
    seeder.add_entity(
        Produits,
        5,
        {
            'nom': lambda x: seeder.faker.name(),
            'image_1': 'produits/image1.jpg',
            'image_2': 'produits/image2.jpg',
            'image_3': 'produits/image3.jpg',
            'image_4': 'produits/image4.jpg',
            'image_5': 'produits/image5.jpg',
            'image_6': 'produits/image6.jpg',
            'marque_vendeur': lambda x: seeder.faker.name(),
            'type': lambda x: seeder.faker.random_element(['gélules', 'poudre']),
            'categorie': lambda x: seeder.faker.random_element(Categorie.objects.all()),
            'description': lambda x: seeder.faker.paragraph(),
            'ingredients': lambda x: seeder.faker.paragraph(),
            'macronutriments': lambda x: seeder.faker.paragraph(),
            'variations': lambda x: seeder.faker.word(),
            'en_promo': lambda x: seeder.faker.boolean(),
            'nature_promo': lambda x: seeder.faker.random_element(Promotions.objects.all()),
            'pourcentage_promo': lambda x: seeder.faker.random_int(min=0, max=100),
            'prix_normal': lambda x: seeder.faker.random_int(min=0, max=100),
            'prix_promo': lambda x: seeder.faker.random_int(min=0, max=100),
            'quantite_stock': lambda x: seeder.faker.random_int(min=0, max=100),
        },
    )

    # Seed Commentaires
    seeder.add_entity(
        Commentaires,
        5,
        {
            'user': lambda x: seeder.faker.random_element(User.objects.all()),
            'date': lambda x: seeder.faker.date_time_this_year(),
            'reponse_a': lambda x: seeder.faker.random_element(Commentaires.objects.all()),
            'produit_associe': lambda x: seeder.faker.random_element(Produits.objects.all()),
            'blog_post_associe': lambda x: seeder.faker.random_element(BlogPost.objects.all()),
        },
    )

    # Seed Avatar
    seeder.add_entity(
        Avatar,
        5,
        {
            'image_avatar': 'avatars/avatar.jpg',
            'users_lies': lambda x: seeder.faker.random_elements(User.objects.all(), seeder.faker.random_int(min=1, max=5)),
        },
    )

    # Seed Tags
    seeder.add_entity(
        Tags,
        5,
        {
            'nom': lambda x: seeder.faker.name(),
            'blog_posts_lies': lambda x: seeder.faker.random_elements(BlogPost.objects.all(), seeder.faker.random_int(min=1, max=5)),
        },
    )

   



    # Seed Wishlist
    seeder.add_entity(
        Wishlist,
        5,
        {
            'user': lambda x: seeder.faker.random_element(UserExtension.objects.all()),
            'produits_ajoutes': lambda x: seeder.faker.random_elements(Produits.objects.all(), seeder.faker.random_int(min=1, max=5)),
        },
    )


    # Seed BlogPost
    seeder.add_entity(
        BlogPost,
        5,
        {
            'titre': lambda x: seeder.faker.sentence(),
            'texte': lambda x: seeder.faker.paragraph(),
            'categorie': lambda x: seeder.faker.random_element(Categorie.objects.all()),
            'image_illustration': 'blogposts/image.jpg',
            'date_post': lambda x: seeder.faker.date_this_year(),
            'date_modification': lambda x: seeder.faker.date_this_month(),
            'user_auteur': lambda x: seeder.faker.random_element(User.objects.all()),
            'review_blogpost': lambda x: seeder.faker.random_element(Review.objects.all()),
        },
    )

    # Seed Review
    seeder.add_entity(
        Review,
        5,
        {
            'note_moyenne': lambda x: seeder.faker.random_int(min=1, max=5),
            'produit_ou_blogpost_lie': lambda x: seeder.faker.random_element(Produits.objects.all()),
        },
    )
    
    # Seed InfosQDP
    seeder.add_entity(
        InfosQDP,
        5,
        {
            'adresse': lambda x: seeder.faker.address(),
            'email': lambda x: seeder.faker.email(),
            'telephone': lambda x: seeder.faker.phone_number(),
            'fax': lambda x: seeder.faker.phone_number(),
            'slogan_site': lambda x: seeder.faker.sentence(),
        },
    )

    # Seed Partenaires
    seeder.add_entity(
        Partenaires,
        5,
        {
            'nom': lambda x: seeder.faker.name(),
            'logo': 'partenaires/logo.jpg',
        },
    )

    inserted_pks = seeder.execute()
    print(inserted_pks)
