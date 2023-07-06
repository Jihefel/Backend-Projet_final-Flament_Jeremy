# Produits
- Nom
- 6 images
- marque/vendeur
- type (gélules ou poudre)
- catégorie (foreign key)
- description
- ingredients (tableau)
- macronutriments
- variations (grammage si poudre ou nombre de gélules)
- en promo ? (boolean)
- si promo = true : nature de la promo (foreign key)
- si promo = true : pourcentage en promo (foreign key)
- prix normal
- prix en promo
- quantité en stock pour chaque variation
- review du produit
- commentaire (foreign key ? avec commentaire lié à l'id du produit)
- date d'ajout du produit dans la db
- date d'ajout du produit dans le panier du user
- date d'ajout du produit dans la wishlist

# Catégorie
- nom de la categorie (protéines, acides aminés, vitamines, compléments, bruleurs de graisses)
- promo ou pas ? (boolean)
- pourcentage de la promo si en promo
(si une catégorie est en promo, tous les produits de cette catégorie sont en promo. Les produits peuvent être individuellement en promo sans que leur catégorie ne soit en promo. )

# Promotions
- Nom de la promo
- Pourcentage de promotion
- Slogan
- Description
- Image d'illustration
- date de début (jour/mois)
- date de fin (jour/mois)
- categorie en promo (foreign key)
- produit en promo (foreign key)

# Commentaires
- User
- date (jour et heure)
- Réponses (un commentaire peut être lié à un autre, une réponse à l'un)
- id du blog post ou du produit lié (donc 2 colonnes surement ? l'une null et l'autre pas - foreign key)

# Wishlist
- User concerné
- Produits ajoutés dans la wishlist du user

# Avatar
- Image de l'avatar
- users liés

# Tags
- Nom
- Blog posts liés

# User
- Model user de base de django
+ Avatar lié
+ Métiers ou hobbies
+ Bio (texte)
+ Image de bannière de profil
+ produits dans le panier
+ produits dans la wishlist
+ commandes passées
+ contacts échangés entre les admin et les user
+ abonné à la newsletter ? (boolean, defaut : false)

# Group
- Model Groupe de base de django (lié à l'user) (le 1er user créé est d'office un admin, les autres sont Membre)
Admin peut tout faire sauf supprimer les autres user "Admin" que lui. Webmaster peut 

# Panier
- User concerné (foreign key)
- produits inclus (foreign key)
- quantité ajoutée du produit

# Commandes
- User (foreign key)
- date de la commande
- produits commandés qui étaient dans le panier (si commandés, ceux du panier sont vidés)
- statut de la commande (confirmée ou non) (boolean)

# Review
- note moyenne 1-5
- Blog post ou produit lié

# Blog post
- Titre
- Texte du blog post
- Catégorie (foreign key)
- Image d'illustration
- Date du post (création + modification)
- Commentaires liés
- User (auteur du post)
- review du blog post

# Contacts
- User (auteur du contact) (peux être null)
- Texte
- si user null :
    - Name
    - email

# Infos QDP
- Adresse
- Email
- Téléphone
- Fax
- Slogan du site

# Partenaires
- Nom
- Logo

# Change password
- Model de base pour changer password
- old password n'est pas demandé

# Newsletter
- email 
- (si un email rentré correspond à un email d'un user, l'user est associé à la newsletter (abonné à la newsletter = True) et n'est pas rajouté (foreign key))