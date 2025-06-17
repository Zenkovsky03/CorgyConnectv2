"""
Funkcje pomocnicze i factory do tworzenia testowych instancji modeli
dla aplikacji `doggs`.

Ułatwia tworzenie danych testowych dla testów jednostkowych.
"""

import factory
from django.contrib.auth.models import User
from django.db.models import signals

from users.models import Profile
from doggs.models import Dog, Tag, Review


# 1️⃣  NIE uruchamiamy sygnału post_save → profil NIE powstaje automatycznie
@factory.django.mute_signals(signals.post_save)
class UserFactory(factory.django.DjangoModelFactory):
    """
    Fabryka użytkowników Django.

    Tworzy użytkownika bez automatycznego tworzenia profilu,
    dzięki wyciszeniu sygnałów post_save.
    """
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "pass")


# 2️⃣  Profil tworzymy świadomie i zawsze z tym samym user_id
class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Fabryka profili użytkowników.

    Tworzy profil na podstawie użytkownika wygenerowanego przez UserFactory.
    """
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)


# 3️⃣  Pies dostaje właściciela = istniejący profil
class DogFactory(factory.django.DjangoModelFactory):
    """
    Fabryka psów.

    Generuje przykładowego psa z przypisanym właścicielem (Profile).
    """
    class Meta:
        model = Dog

    owner = factory.SubFactory(ProfileFactory)
    name  = factory.Faker("first_name")
    description = factory.Faker("sentence")


class TagFactory(factory.django.DjangoModelFactory):
    """
    Fabryka tagów.

    Generuje unikalne tagi tekstowe.
    """
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f"tag{n}")


class ReviewFactory(factory.django.DjangoModelFactory):
    """
    Fabryka opinii (recenzji).

    Tworzy recenzję przypisaną do psa i profilu użytkownika.
    """
    class Meta:
        model = Review

    owner = factory.SubFactory(ProfileFactory)
    dog   = factory.SubFactory(DogFactory)
    value = "up"
    body  = factory.Faker("sentence")
