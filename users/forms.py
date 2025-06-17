"""
Formularze Django dla aplikacji `users`.

Zawiera:
- `SkillForm`: formularz do dodawania i edycji umiejętności
- `MessageForm`: formularz do wysyłania wiadomości między użytkownikami

Dodaje wspólną klasę CSS do wszystkich pól (`input`).
"""


from django.contrib.auth.views import PasswordResetView
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill, Message

from ckeditor.widgets import CKEditorWidget
from django import forms



class CustomUserCreationForm(UserCreationForm):
    """
    Formularz rejestracji nowego użytkownika.

    Rozszerza domyślny formularz Django o pola dla modelu User.
    """
    class Meta:
        model = User
        fields = ('first_name', 'email', 'username', 'password1', 'password2')
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class ProfileForm(ModelForm):
    """
    Formularz do edycji profilu użytkownika.

    Umożliwia edycję imienia, nazwiska, adresu e-mail, zdjęcia oraz opisu.
    """
    bio = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Profile
        fields = [
            'name',
            'email',
            'username',
            'location',
            'bio',
            'short_intro',
            'profile_image',
            'social_github',
            'social_website',
            'social_twitter',
            'social_linkedin',
            'social_youtube',
        ]
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class SkillForm(ModelForm):
    """
    Formularz do tworzenia i edytowania obiektów Skill (umiejętności).

    Ukrywa pole 'owner', ponieważ przypisywane jest automatycznie na podstawie zalogowanego użytkownika.
    Dodaje klasę CSS 'input' do każdego pola formularza.
    """
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MessageForm(ModelForm):
    """
    Formularz do tworzenia wiadomości przesyłanych między użytkownikami.

    Umożliwia podanie imienia, e-maila, tematu i treści wiadomości.
    Dodaje klasę CSS 'input' do każdego pola formularza.
    """
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
