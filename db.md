# Produits
- Nom
- 6 images
- marque/vendeur
- type (gélules ou poudre)
- categorie (protéines, acides aminés, vitamines, compléments, bruleurs de graisses)
- description
- ingredients (tableau)
- macronutriments
- variations (grammage si poudre ou nombre de gélules)
- en promo ? (boolean)
- si promo = true : nature de la promo
- si promo = true : pourcentage en promo
- prix normal
- prix en promo
- quantité en stock pour chaque variation
- note moyenne du produit 1-5
- commentaire (foreign key ? avec commentaire lié à l'id du produit)
- date d'ajout du produit

# Promotions
- Nom de la promo
- Pourcentage maximum de promotion
- date de début
- date de fin

# Commentaires
- User
- date (jour et heure)
- Réponses (un commentaire peut être lié à un autre, une réponse à l'un)
- id de l'article ou du produit lié (donc 2 colonnes surement ? l'une null et l'autre pas - foreign key)

# Wishlist
- foreign key du produit
- date d'ajout du produit dans la wishlist

# Panier
- foreign key du produit
- quantité ajoutée du produit
- date d'ajout du produit dans le panier

