"""
Fabryki testowe dla modeli aplikacji `users`.

Zawiera klasy umożliwiające szybkie tworzenie instancji modeli `User`, `Profile`, `Skill` oraz `Message`
na potrzeby testów jednostkowych i integracyjnych. Każda fabryka automatyzuje proces przypisywania
domyślnych wartości atrybutów i powiązań między modelami.
"""
# users/tests/factories.py
import factory
from django.db.models import signals
from django.contrib.auth.models import User
from users.models import Profile, Skill, Message


#user
@factory.django.mute_signals(signals.post_save)           # blokujemy sygnał -> profil robimy sami
class UserFactory(factory.django.DjangoModelFactory):
    """
    Fabryka do tworzenia użytkowników `User`.
    Sygnały są wyciszane, aby uniknąć automatycznego tworzenia profili.
    """
    class Meta:
        model = User

    username  = factory.Sequence(lambda n: f"user{n}")
    password  = factory.PostGenerationMethodCall("set_password", "pass")
    first_name = factory.Faker("first_name")
    email      = factory.LazyAttribute(lambda o: f"{o.username}@example.com")


# users/tests/factories.py  (zamień tylko metodę _create w ProfileFactory)

class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Fabryka do tworzenia profili `Profile`.

    Jeżeli nie podano użytkownika, zostanie automatycznie utworzony nowy.
    Wypełnia brakujące dane z przypisanego użytkownika.
    """
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Niestandardowe tworzenie profilu z obsługą brakujących danych.
        """
        user = kwargs.pop("user", None) or UserFactory()
        profile, _ = Profile.objects.get_or_create(user=user)

        # atrybuty przekazane z create()/create_batch
        for field, value in kwargs.items():
            setattr(profile, field, value)

        # --- wypełniamy wymagane lub filtrowane pola, jeśli puste ---
        if not profile.username:
            profile.username = user.username
        if not profile.email:
            profile.email = user.email
        if not profile.name:              #  ← KLUCZOWE
            profile.name = user.first_name or user.username

        profile.save()                    # zapis (uruchomi sygnał)
        return profile




#skill
class SkillFactory(factory.django.DjangoModelFactory):
    """
    Fabryka do tworzenia umiejętności `Skill` powiązanych z profilem.
    """
    class Meta:
        model = Skill

    owner = factory.SubFactory(ProfileFactory)
    name  = factory.Sequence(lambda n: f"skill{n}")
    description = ""


#message
class MessageFactory(factory.django.DjangoModelFactory):
    """
    Fabryka do tworzenia wiadomości `Message` pomiędzy profilami.
    """
    class Meta:
        model = Message

    sender    = factory.SubFactory(ProfileFactory)
    recipient = factory.SubFactory(ProfileFactory)
    subject   = factory.Sequence(lambda n: f"Hello {n}")
    body      = factory.Faker("sentence")
