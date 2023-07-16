from django import forms
from .models import *
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
        fields = ['image_banniere_profil', 'avatar', 'first_name', 'last_name', 'email', 'username', 'metiers_hobbies', 'bio' ]
        widgets = {
            'image_banniere_profil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class UserCreationForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Roles.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='role',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter a strong password."
    )
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role', 'image_banniere_profil', 'avatar', 'metiers_hobbies', 'bio', 'abonne_newsletter']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'image_banniere_profil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'metiers_hobbies': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'abonne_newsletter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserUpdateForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Roles.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='role',
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'image_banniere_profil', 'avatar', 'metiers_hobbies', 'bio', 'abonne_newsletter']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'image_banniere_profil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'metiers_hobbies': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'abonne_newsletter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }

class UserRoleUpdateForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Roles.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='role',
    )
    class Meta:
        model = User
        fields = ['role']


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'promo', 'slogan', 'description', 'image_illustration']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'promo': forms.Select(attrs={'class': 'form-control'}),
            'slogan': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image_illustration': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class PromotionsForm(forms.ModelForm):
    class Meta:
        model = Promotions
        fields = ['nom', 'pourcentage_promo', 'date_debut', 'date_fin']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'pourcentage_promo': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_illustration': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
        }

class ExtraPromotionForm(forms.ModelForm):
    class Meta:
        model = ExtraPromo
        fields = ['extra_promo']
        widgets = {
            'extra_promo': forms.Select(attrs={'class': 'form-control'})
        }

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['quantite_stock', 'prix']
        widgets = {
            'contenu': forms.TextInput(attrs={'class': 'form-control'}),
            'quantite_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProduitsForm(forms.ModelForm):
    class Meta:
        model = Produits
        fields = ['nom', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'marque_vendeur', 'type', 'categorie', 'description', 'ingredients', 'macronutriments', 'promo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'image_1': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image_2': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image_3': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image_4': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image_5': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'marque_vendeur': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'macronutriments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'promo': forms.Select(attrs={'class': 'form-control'}),
        }


class VariantForm(forms.ModelForm):
    class Meta:
        model = Variantes
        fields = ['contenu']
        widgets = {
            'contenu': forms.Select(attrs={'class': 'col-form-label border-0'})
        } 

class PriceFilterForm(forms.Form):
    filter_by_price = forms.IntegerField(
        label='Filter by Price',
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': 0,
            'max': 100,
            'step': 5,
            'value': 100,
            'list': 'values',
            'style': "accent-color: #f53f85",
            'class': "w-100"
        }),
        required=False
    )

class NameFilterForm(forms.Form):
    filter_by_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name',
            'autocomplete': 'off',
        })
    )

class CommentairesForm(forms.ModelForm):
    class Meta:
        model = Commentaires
        fields = ['user', 'reponse_a']

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

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['titre', 'texte', 'categorie', 'image_illustration', 'date_post', 'date_modification', 'commentaires_lies', 'user_auteur']
        exclude = ['date_post', 'date_modification']

class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['user_auteur', 'name', 'email', 'texte']

class InfosQDPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['adresse'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Adresse'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['telephone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Téléphone'})
        self.fields['fax'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Fax'})
        self.fields['slogan_site'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Slogan du site'})

    class Meta:
        model = InfosQDP
        fields = ['adresse', 'email', 'telephone', 'fax', 'slogan_site']


class PartenairesForm(forms.ModelForm):
    class Meta:
        model = Partenaires
        fields = ['nom', 'logo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(label='Your E-mail Address:', widget=forms.EmailInput(attrs={'class': 'input-newsletter', 'placeholder': 'Enter your email', 'required': True, 'autocomplete': 'off'}))
    
    class Meta:
        model = Newsletter
        fields = ['email']

class SignupForm2(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'metiers_hobbies', 'bio', 'image_banniere_profil', 'abonne_newsletter']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control', 'type': 'file'}),
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