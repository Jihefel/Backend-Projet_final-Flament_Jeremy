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
    inserted_pks = seeder.execute()
    print(inserted_pks)