from django.db import models
from django.contrib.auth.models import AbstractUser

    
class Roles(models.Model):
    ADMIN = 'admin'
    MEMBRE = 'membre'
    WEB = 'webmaster'
    STOCK = 'stock'
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MEMBRE, 'Membre'),
        (WEB, 'Webmaster'),
        (STOCK, 'Stock'),
    )
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)
    def __str__(self):
        return self.get_role_display()

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=True, default=2)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    metiers_hobbies = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image_banniere_profil = models.ImageField(upload_to='bannieres/', null=True, blank=True)
    produits_panier = models.ManyToManyField('Produits', related_name='paniers')
    produits_wishlist = models.ManyToManyField('Produits', related_name='wishlists')
    commandes_passees = models.ManyToManyField('Commandes',related_name='commandes')
    contacts_echanges = models.ManyToManyField('Contacts', related_name='contacts')
    abonne_newsletter = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    promo = models.BooleanField(default=False)
    pourcentage_promo = models.PositiveIntegerField(null=True, blank=True)

class Promotions(models.Model):
    nom = models.CharField(max_length=255)
    pourcentage_promo = models.PositiveIntegerField()
    slogan = models.CharField(max_length=255)
    description = models.TextField()
    image_illustration = models.ImageField(upload_to='promotions/')
    date_debut = models.DateField()
    date_fin = models.DateField()
    categorie_en_promo = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True)
    produit_en_promo = models.ForeignKey('Produits', on_delete=models.CASCADE, null=True, blank=True)

class Produits(models.Model):
    nom = models.CharField(max_length=255)
    image_1 = models.ImageField(upload_to='produits/')
    image_2 = models.ImageField(upload_to='produits/')
    image_3 = models.ImageField(upload_to='produits/')
    image_4 = models.ImageField(upload_to='produits/')
    image_5 = models.ImageField(upload_to='produits/')
    image_6 = models.ImageField(upload_to='produits/')
    marque_vendeur = models.CharField(max_length=255)
    TYPE_CHOICES = (
        ('gélules', 'Gélules'),
        ('poudre', 'Poudre'),
    )
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    description = models.TextField()
    ingredients = models.TextField()
    macronutriments = models.TextField()
    variations = models.CharField(max_length=255)
    en_promo = models.BooleanField(default=False)
    nature_promo = models.ForeignKey(Promotions, null=True, blank=True, on_delete=models.CASCADE)
    pourcentage_promo = models.PositiveIntegerField(null=True, blank=True)
    prix_normal = models.DecimalField(max_digits=10, decimal_places=2)
    prix_promo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantite_stock = models.PositiveIntegerField()
    review_produit = models.ForeignKey('Review', null=True, blank=True, on_delete=models.CASCADE)
    commentaire = models.ForeignKey('Commentaires', null=True, blank=True, on_delete=models.CASCADE)
    date_ajout_produit_db = models.DateField(auto_now_add=True)
    date_ajout_panier_user = models.DateField(null=True, blank=True)
    date_ajout_wishlist_user = models.DateField(null=True, blank=True)

class Commentaires(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    reponse_a = models.ForeignKey('Commentaires', null=True, blank=True, on_delete=models.CASCADE)
    produit_associe = models.ForeignKey(Produits, null=True, blank=True, on_delete=models.CASCADE)
    blog_post_associe = models.ForeignKey('BlogPost', null=True, blank=True, on_delete=models.CASCADE)

class Tags(models.Model):
    nom = models.CharField(max_length=255)
    blog_posts_lies = models.ManyToManyField('BlogPost')
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produits_ajoutes = models.ManyToManyField(Produits)

class Panier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit_inclus = models.ForeignKey(Produits, on_delete=models.CASCADE)
    quantite_ajoutee = models.PositiveIntegerField()

class Commandes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commande = models.DateField()
    produits_commandes = models.ManyToManyField(Produits, through='ProduitsCommandes')
    statut_commande = models.BooleanField(default=False)

class ProduitsCommandes(models.Model):
    commande = models.ForeignKey(Commandes, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)

class Review(models.Model):
    note_moyenne = models.DecimalField(max_digits=2, decimal_places=1)
    produit_ou_blogpost_lie = models.ForeignKey(Produits, on_delete=models.CASCADE, null=True, blank=True)

class BlogPost(models.Model):
    titre = models.CharField(max_length=255)
    texte = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    image_illustration = models.ImageField(upload_to='blogposts/')
    date_post = models.DateField(auto_now_add=True)
    date_modification = models.DateField(auto_now=True)
    commentaires_lies = models.ManyToManyField(Commentaires)
    user_auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    review_blogpost = models.ForeignKey(Review, null=True, blank=True, on_delete=models.CASCADE)

class Contacts(models.Model):
    user_auteur = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    texte = models.TextField()

class InfosQDP(models.Model):
    adresse = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    slogan_site = models.CharField(max_length=255)

class Partenaires(models.Model):
    nom = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='partenaires/')

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    user_associated = models.ManyToManyField(User, blank=True)

