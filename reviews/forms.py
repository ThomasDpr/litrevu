from django import forms
from django.contrib.auth import get_user_model

from .models import Review, Ticket, UserFollows


class TicketForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
            'placeholder': 'Titre du livre/article'
        }),
        label='Titre',
        error_messages={
            'required': 'Le titre est obligatoire.'
        }
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
            'rows': '4',
            'placeholder': 'Description du livre/article'
        }),
        label='Description',
        error_messages={
            'required': 'La description est obligatoire.'
        }
    )
    
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            'accept': 'image/*'
        }),
        label='Image',
        required=False
    )

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class DeleteTicketForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmer la suppression"
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(6)])
        }

class DeleteReviewForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmer la suppression"
    )

# Nouveau formulaire pour suivre un utilisateur
class UserFollowsForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'placeholder': "Entrez le nom d'utilisateur",
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        User = get_user_model()

        # Vérifie si l'utilisateur existe
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Cet utilisateur n'existe pas.")
        return username
        
        