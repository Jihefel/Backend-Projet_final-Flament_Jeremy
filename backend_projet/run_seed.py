import django
django.setup()

from shop.seed import run

if __name__== '__main__':
    run()
