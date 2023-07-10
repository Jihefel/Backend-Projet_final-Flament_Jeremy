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
    roles = ['admin', 'membre', 'webmaster', 'stock']

    # Seed Group
    seeder.add_entity(
        Roles,
        len(roles),
        {
            'role': lambda x, roles_iter=itertools.cycle(roles): next(roles_iter),
        },
    )

    seeder.add_entity(InfosQDP, 1, {
        'adresse': 'Wonder Street, USA, New York',
        'email': 'hello@xton.com',
        'telephone': '+01 321 654 214',
        'fax': '+123456789',
        'slogan_site': 'One of the most popular on the web is shopping. Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    })
    inserted_pks = seeder.execute()
    print(inserted_pks)