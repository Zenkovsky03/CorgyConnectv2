"""
Modele danych aplikacji `users`, rozszerzające domyślny model użytkownika Django.

Zawiera:
- `Profile`: dane rozszerzające użytkownika (`User`)
- `Skill`: umiejętności użytkownika
- `Message`: wiadomości wysyłane między użytkownikami
"""

from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
class Profile(models.Model):
    """
    Reprezentuje profil użytkownika powiązany z obiektem User.

    Przechowuje dodatkowe informacje takie jak imię, nazwisko, lokalizacja,
    krótki opis (bio), linki społecznościowe i obraz profilowy.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    @property
    def imageURL(self):
        try:
            url= self.profile_image.url
        except:
            url = " "
        return url

    class Meta:
        ordering = ['created']

class Skill(models.Model):
    """
    Umiejętność przypisana do konkretnego profilu użytkownika.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Reprezentuje wiadomość wysyłaną pomiędzy użytkownikami aplikacji.

    Pola:
        sender (Profile): Nadawca wiadomości (może być null, np. od gościa).
        recipient (Profile): Odbiorca wiadomości.
        name (str): Imię nadawcy (jeśli nie jest zarejestrowanym użytkownikiem).
        email (str): Adres e-mail nadawcy.
        subject (str): Temat wiadomości.
        body (str): Treść wiadomości.
        is_read (bool): Czy wiadomość została przeczytana przez odbiorcę.
        created (datetime): Znacznik czasu utworzenia wiadomości.

    Wiadomości są sortowane według daty utworzenia (najnowsze pierwsze).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages') #taki jakby placeholder ze to sa wiadomosci usera
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']