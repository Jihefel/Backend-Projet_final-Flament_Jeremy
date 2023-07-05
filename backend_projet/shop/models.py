from django.db import models

class Pays(models.Model):
    nom = models.CharField(max_length=255)
    population = models.IntegerField()

    def __str__(self):
        return self.nom


class President(models.Model):
    GENRE_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )

    nom = models.CharField(max_length=255)
    age = models.IntegerField()
    image = models.ImageField(upload_to='presidents/')
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom
