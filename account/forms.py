from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignupForm(UserCreationForm):

    username = forms.CharField(
        error_messages={
            'required': 'Le nom d\'utilisateur est obligatoire.',
            'unique': 'Ce nom d\'utilisateur est déjà pris.',
            'invalid': 'Ce nom d\'utilisateur contient des caractères invalides.',
        },
        widget=forms.TextInput(
            attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': "Nom d'utilisateur",
            }
        ),
        help_text='150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement.',
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Mot de passe',
            }
        ),
        help_text='Votre mot de passe doit contenir au moins 8 caractères.',
        error_messages={'required': 'Le mot de passe est obligatoire.'},
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Confirmation du mot de passe',
            }
        ),
        help_text='Entrez le même mot de passe que précédemment.',
        error_messages={'required': 'La confirmation du mot de passe est obligatoire.'},
    )

    error_messages = {'password_mismatch': 'Les deux mots de passe ne correspondent pas.'}

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        error_messages={'required': 'Ce champ est obligatoire.'},
        widget=forms.TextInput(
            attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': "Nom d'utilisateur",
            }
        ),
        label="Nom d'utilisateur",
    )
    password = forms.CharField(
        error_messages={'required': 'Ce champ est obligatoire.'},
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Mot de passe',
            }
        ),
        label="Mot de passe",
    )

    error_messages = {
        'invalid_login': "Nom d'utilisateur ou mot de passe incorrect.",
        'inactive': "Ce compte est inactif.",
    }
