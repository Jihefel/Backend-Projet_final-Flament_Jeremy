from django_seed import Seed    
from shop.models import Pays, President
import random
import os

def run():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_projet.settings')
    seeder = Seed.seeder()
    
    # Seed pour le modèle Pays
    seeder.add_entity(Pays, 5, {
        'nom': lambda x: seeder.faker.country(),
        'population': lambda x: seeder.faker.random_int(min=1000, max=1000000)
    })

    # Seed pour le modèle President
    seeder.add_entity(President, 5, {
        'nom': lambda x: seeder.faker.name(),
        'age': lambda x: seeder.faker.random_int(min=30, max=80),
        'genre': lambda x: seeder.faker.random_element(['M', 'F']),
        'pays': lambda x: seeder.faker.random_element(Pays.objects.all())
    })

    inserted_pks = seeder.execute()
    print(inserted_pks)
