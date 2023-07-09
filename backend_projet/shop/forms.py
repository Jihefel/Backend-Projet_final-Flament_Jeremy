from django import forms
from .models import User, Categorie, Promotions, ProduitsCommandes, Panier, Partenaires, Produits, Wishlist, Avatar, Commentaires, Roles, Tags, Review, Commandes, BlogPost, Newsletter, Contacts, InfosQDP
from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']

class BootstrapUserCreationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm your password'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your email address'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your first name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your last name'})

class SignupForm(forms.Form):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

class EditProfileForm(forms.ModelForm):
    metiers_hobbies = forms.CharField(label="Jobs or hobbies", widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['image_banniere_profil', 'avatar_lie', 'first_name', 'last_name', 'email', 'username', 'metiers_hobbies', 'bio' ]
        widgets = {
            'image_banniere_profil': forms.FileInput(attrs={'class': 'form-control-file'}),
            'avatar_lie': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'promo', 'pourcentage_promo']

class PromotionsForm(forms.ModelForm):
    class Meta:
        model = Promotions
        fields = ['nom', 'pourcentage_promo', 'slogan', 'description', 'image_illustration', 'date_debut', 'date_fin', 'categorie_en_promo', 'produit_en_promo']

class ProduitsForm(forms.ModelForm):
    class Meta:
        model = Produits
        fields = ['nom', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6', 'marque_vendeur', 'type', 'categorie', 'description', 'ingredients', 'macronutriments', 'variations', 'en_promo', 'nature_promo', 'pourcentage_promo', 'prix_normal', 'prix_promo', 'quantite_stock', 'review_produit', 'commentaire', 'date_ajout_produit_db', 'date_ajout_panier_user', 'date_ajout_wishlist_user']
        exclude = ['date_ajout_produit_db']

class CommentairesForm(forms.ModelForm):
    class Meta:
        model = Commentaires
        fields = ['user', 'reponse_a', 'produit_associe', 'blog_post_associe']

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['user', 'produits_ajoutes']

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image_avatar']
class TagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['nom', 'blog_posts_lies']

class RolesForm(forms.ModelForm):
    class Meta:
        model = Roles
        fields = ['role']

class PanierForm(forms.ModelForm):
    class Meta:
        model = Panier
        fields = ['user', 'produit_inclus', 'quantite_ajoutee']

class CommandesForm(forms.ModelForm):
    class Meta:
        model = Commandes
        fields = ['user', 'date_commande', 'produits_commandes', 'statut_commande']

class ProduitsCommandesForm(forms.ModelForm):
    class Meta:
        model = ProduitsCommandes
        fields = ['commande', 'produit']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['note_moyenne', 'produit_ou_blogpost_lie']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['titre', 'texte', 'categorie', 'image_illustration', 'date_post', 'date_modification', 'commentaires_lies', 'user_auteur', 'review_blogpost']
        exclude = ['date_post', 'date_modification']

class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['user_auteur', 'name', 'email', 'texte']

class InfosQDPForm(forms.ModelForm):
    class Meta:
        model = InfosQDP
        fields = ['adresse', 'email', 'telephone', 'fax', 'slogan_site']

class PartenairesForm(forms.ModelForm):
    class Meta:
        model = Partenaires
        fields = ['nom', 'logo']

class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(label='Your E-mail Address:', widget=forms.EmailInput(attrs={'class': 'input-newsletter', 'placeholder': 'Enter your email', 'required': True, 'autocomplete': 'off'}))
    
    class Meta:
        model = Newsletter
        fields = ['email']

class SignupForm2(forms.ModelForm):
    avatar_lie = forms.ModelChoiceField(queryset=Avatar.objects.all(), widget=forms.RadioSelect, required=False)
    
    class Meta:
        model = User
        fields = ['avatar_lie', 'metiers_hobbies', 'bio', 'image_banniere_profil', 'abonne_newsletter']
        widgets = {
            'metiers_hobbies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your jobs or hobbies'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Introduce yourself', 'rows': 4}),
            'image_banniere_profil': forms.ClearableFileInput(attrs={'class': 'form-control', 'type': 'file'}),
            'abonne_newsletter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'