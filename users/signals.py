"""
Sygnały Django odpowiedzialne za tworzenie, aktualizację i usuwanie powiązań
pomiędzy obiektem `User` a jego `Profile`.

Rejestruje sygnały:
- `post_save` na `User` → tworzy nowy profil
- `post_save` na `Profile` → aktualizuje użytkownika
- `post_delete` na `Profile` → usuwa użytkownika
"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

#@receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    """
    Tworzy obiekt Profile dla nowo utworzonego użytkownika (User).

    Dodatkowo wysyła wiadomość powitalną na e-mail.

    Args:
        sender (Model): Model, który wysłał sygnał (User).
        instance (User): Obiekt użytkownika.
        created (bool): Czy obiekt został właśnie utworzony.
        **kwargs: Dodatkowe argumenty kontekstowe.
    """
    print("Profile signal triggered")
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        subject = 'Welcome to CorgyConnect'
        message = 'Thanks for signing and support our community! '
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently = False,
        )



def updateUser(sender, instance, created ,**kwargs):
    """
    Aktualizuje dane obiektu User na podstawie zmian w obiekcie Profile.

    Args:
        sender (Model): Model, który wysłał sygnał (Profile).
        instance (Profile): Obiekt profilu.
        created (bool): Czy profil został właśnie utworzony.
        **kwargs: Dodatkowe argumenty kontekstowe.
    """
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    """
    Usuwa obiekt User, jeśli odpowiadający mu obiekt Profile został usunięty.

    Args:
        sender (Model): Model, który wysłał sygnał (Profile).
        instance (Profile): Usunięty obiekt profilu.
        **kwargs: Dodatkowe argumenty kontekstowe.
    """
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)