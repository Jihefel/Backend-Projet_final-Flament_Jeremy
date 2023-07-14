from django_seed import Seed    
from shop.models import *
import random
from django.contrib.auth.hashers import make_password
import itertools
from datetime import date

def run():
    seeder = Seed.seeder()

    User.objects.all().delete()
    Roles.objects.all().delete()
    InfosQDP.objects.all().delete()
    Categorie.objects.all().delete()
    Produits.objects.all().delete()
    Partenaires.objects.all().delete()
    
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
        'slogan_site': lambda x: seeder.faker.catch_phrase() 
    })

    inserted_pks = seeder.execute()
    print(inserted_pks)


    
    # Configurer le seed pour le modèle Promotions
    seeder.add_entity(
        Promotions,
        5,  # Nombre de promotions à générer
        {
            'nom': lambda x: seeder.faker.word(),
            'pourcentage_promo': lambda x: random.randint(5, 90),
            'slogan': lambda x: seeder.faker.sentence(),
            'description': lambda x: seeder.faker.paragraph(),
            'image_illustration': lambda x: seeder.faker.image_url(width=1920, height=1080),  # Chemin de l'image d'illustration
            'date_debut': lambda x: random.choice([date.today(), seeder.faker.date()]),
            'date_fin': lambda x: seeder.faker.future_date(),
        }
    )

    # Exécuter le seed
    inserted = seeder.execute()
    print(inserted)



    # Seed Categories
    categories = [
        'Proteins',
        'Amino acids',
        'Vitamins',
        'Supplements',
        'Fat burners',
    ]

    seeder.add_entity(
        Categorie,
        len(categories),
        {
            'nom': lambda x, categories_iter=itertools.cycle(categories): next(categories_iter),
            'promo': lambda x: None if random.choice([True, False]) else random.choice(Promotions.objects.all()),
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
        'type': lambda x: random.choice(['capsules', 'powder']),
        'categorie': lambda x: random.choice(Categorie.objects.all()),
        'description': lambda x: seeder.faker.paragraph(),
        'ingredients': lambda x: seeder.faker.text(),
        'macronutriments': lambda x: seeder.faker.text(),
        'promo' : lambda x: None if random.choice([True, False]) else random.choice(Promotions.objects.all()),
    })

    inserted_pks = seeder.execute()

    # Seed partenaires
    seeder.add_entity(Partenaires, 6, {
        'nom': lambda x: seeder.faker.company(),
        'logo': lambda x: seeder.faker.image_url(width=90, height=80)
    })

    inserted = seeder.execute()
    print(inserted)


   # Créer les variantes
    contenus = ['250g', '500g', '1kg', '2kg', '30 capsules', '60 capsules', '90 capsules', '120 capsules']
    for contenu in contenus:
        variant = Variantes.objects.create(contenu=contenu)

    # Associer les variants aux produits
    for pk in inserted_pks[Produits]:
        produit = Produits.objects.get(pk=pk)

        if produit.type == 'capsules':
            contenus_capsules = ['30 capsules', '60 capsules', '90 capsules', '120 capsules']
            for contenu in contenus_capsules:
                variant = Variantes.objects.get(contenu=contenu)
                ProductVariant.objects.create(product=produit, variant=variant, quantite_stock=random.randint(0, 50), prix=random.uniform(10, 100))
        else:
            contenus_powder = ['250g', '500g', '1kg', '2kg']
            for contenu in contenus_powder:
                variant = Variantes.objects.get(contenu=contenu)
                ProductVariant.objects.create(product=produit, variant=variant, quantite_stock=random.randint(0, 50), prix=random.uniform(10, 100))