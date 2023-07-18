from django.db import models
from django.contrib.auth.models import AbstractUser
import os
    
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
    produits_wishlist = models.ManyToManyField('Produits', related_name='wishlists', blank=True)
    commandes_passees = models.ManyToManyField('Commandes',related_name='commandes', blank=True)
    abonne_newsletter = models.BooleanField(default=False)
    promo_code_used = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Promotions(models.Model):
    nom = models.CharField(max_length=255)
    pourcentage_promo = models.PositiveIntegerField()
    slogan = models.CharField(max_length=255, null=True, blank=True)
    image_illustration = models.ImageField(upload_to='promotions/')
    date_debut = models.DateField()
    date_fin = models.DateField()
    def __str__(self):
        return f"{self.nom} - {self.pourcentage_promo}%"

class ExtraPromo(models.Model):
    extra_promo = models.ForeignKey(Promotions, blank=True, on_delete=models.CASCADE)

class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    promo = models.ForeignKey(Promotions, null=True, blank=True, on_delete=models.SET_NULL)
    slogan = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image_illustration = models.ImageField(upload_to='categories/')
    def __str__(self):
        return self.nom

class Variantes(models.Model): 
    CONTENU_CHOICES = [
        ('250g', '250g'),
        ('500g', '500g'),
        ('1kg', '1kg'),
        ('2kg', '2kg'),
        ('30 capsules', '30 capsules'),
        ('60 capsules', '60 capsules'),
        ('90 capsules', '90 capsules'),
        ('120 capsules', '120 capsules'),
    ]
    contenu = models.CharField(max_length=255, choices=CONTENU_CHOICES, blank=True)
    produits = models.ManyToManyField("Produits", through='ProductVariant', related_name='variante_produits', blank=True)
    def __str__(self):
        return self.contenu

def upload_to_product(instance, filename):
    # Récupérer l'ID du produit
    product_id = instance.id

    # Construire le chemin d'upload avec l'ID du produit
    upload_path = f"produits/{product_id}/{filename}"

    return upload_path

class Produits(models.Model):
    nom = models.CharField(max_length=255)
    image_1 = models.ImageField(upload_to=upload_to_product)
    image_2 = models.ImageField(upload_to=upload_to_product)
    image_3 = models.ImageField(upload_to=upload_to_product)
    image_4 = models.ImageField(upload_to=upload_to_product)
    image_5 = models.ImageField(upload_to=upload_to_product)
    def delete(self, *args, **kwargs):
        # Delete the associated image files
        image_files = [
            self.image_1.path,
            self.image_2.path,
            self.image_3.path,
            self.image_4.path,
            self.image_5.path,
        ]
        for file_path in image_files:
            if os.path.exists(file_path):
                os.remove(file_path)

        # Call the parent's delete method to delete the instance from the database
        super().delete(*args, **kwargs)
    MARQUE_CHOICES = (
        ('MyProtein', 'MyProtein'),
        ('Prozis', 'Prozis'),
        ('HSN', 'HSN'),
        ('Optimum Nutrition', 'Optimum Nutrition'),
        ('MuscleTech', 'MuscleTech'),
        ('Dymatize', 'Dymatize'),
        ('Cellucor', 'Cellucor'),
        ('MusclePharm', 'MusclePharm'),
        ('Universal Nutrition', 'Universal Nutrition'),
    )
    marque_vendeur = models.CharField(max_length=255, choices=MARQUE_CHOICES)
    TYPE_CHOICES = (
        ('capsules', 'Capsules'),
        ('powder', 'Powder'),
    )
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    description = models.TextField()
    ingredients = models.TextField()
    macronutriments = models.TextField()
    variations = models.ManyToManyField(Variantes, through='ProductVariant', related_name='produit_variations', blank=True)
    promo = models.ForeignKey(Promotions, null=True, blank=True, on_delete=models.CASCADE)
    commentaire = models.ManyToManyField('Commentaires', blank=True)
    date_ajout_produit_db = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.id} - {self.nom} "


class ProductVariant(models.Model):
    product = models.ForeignKey(Produits, on_delete=models.CASCADE, null=True, blank=True,)
    variant = models.ForeignKey(Variantes, on_delete=models.CASCADE, null=True, blank=True,)
    quantite_stock = models.PositiveIntegerField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f"{self.variant} ({self.product}): {self.quantite_stock}"
    class Meta:
        unique_together = ('product', 'variant')

class Commentaires(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    reponse_a = models.ForeignKey('Commentaires', null=True, blank=True, on_delete=models.CASCADE)

class Tags(models.Model):
    nom = models.CharField(max_length=255)
    blog_posts_lies = models.ManyToManyField('BlogPost')


class Panier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit_inclus = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantite_ajoutee = models.PositiveIntegerField()

    @property
    def prix_unitaire(self):
        if self.produit_inclus.product.promo:
            prix_promo = float(self.produit_inclus.prix) - (float(self.produit_inclus.prix) * (float(self.produit_inclus.product.promo.pourcentage_promo) / 100))
            return prix_promo
        else:
            return self.produit_inclus.prix
    @property
    def total_individuel(self):
        return self.prix_unitaire * self.quantite_ajoutee
    
    @staticmethod
    def get_total_panier(user):
        if user:
            panier_items = Panier.objects.filter(user=user)
            total = 0.0  # Initialisez le total en tant que float
            for item in panier_items:
                if item.produit_inclus.product.promo:
                    prix_promo = float(item.produit_inclus.prix) - (float(item.produit_inclus.prix) * (float(item.produit_inclus.product.promo.pourcentage_promo) / 100))
                    total += float(prix_promo) * item.quantite_ajoutee  # Convertissez le prix promo en float
                else:
                    total += float(item.produit_inclus.prix) * item.quantite_ajoutee  # Convertissez le prix en float
            return total
    
    @staticmethod
    def calculate_total_final(total_panier, user):
        if user:
            promo_code_name = "kadri"  # Code promo à appliquer
            promo_code_percentage = 10  # Pourcentage de réduction pour le code promo
            shipping_fee = 4.50

            total_final = total_panier + shipping_fee

            if user.promo_code_used:
                    reduction_amount = (promo_code_percentage / 100) * total_panier
                    total_final += reduction_amount
            else:
                total_final = total_panier + shipping_fee

            return total_final
    
    def update_quantity_stock(self, new_quantity):
        old_quantity = self.quantite_ajoutee
        self.quantite_ajoutee = new_quantity
        self.save()

        # Mettre à jour le stock du produit
        diff_quantity = new_quantity - old_quantity
        self.produit_inclus.quantite_stock -= diff_quantity
        self.produit_inclus.save()


    def delete_from_cart(self):
        # Mettre à jour le stock du produit en ajoutant la quantité retirée
        self.produit_inclus.quantite_stock += self.quantite_ajoutee
        self.produit_inclus.save()

        self.delete()

class Commandes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commande = models.DateField()
    produits_commandes = models.ManyToManyField(ProductVariant, through='ProduitsCommandes')
    prix_total = models.DecimalField(decimal_places=2, max_digits=100)
    statut_commande = models.BooleanField(default=False)

class ProduitsCommandes(models.Model):
    commande = models.ForeignKey(Commandes, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

class BlogPost(models.Model):
    titre = models.CharField(max_length=255)
    texte = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    image_illustration = models.ImageField(upload_to='blogposts/')
    date_post = models.DateField(auto_now_add=True)
    date_modification = models.DateField(auto_now=True)
    commentaires_lies = models.ManyToManyField(Commentaires)
    user_auteur = models.ForeignKey(User, on_delete=models.CASCADE)

class Contacts(models.Model):
    user_auteur = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="auteur")
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    texte = models.TextField(null=True)
    lu_par_admin = models.BooleanField(default=False)

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


