"""
Testy widoków aplikacji `doggs`.

Obejmują testy działania endpointów, widoków funkcjonalnych i uprawnień.
"""

import pytest
from django.urls import reverse
from doggs.models import Review
from .factories import DogFactory     # UserFactory ani ProfileFactory nie są tu potrzebne


@pytest.mark.django_db
def test_dogs_view_lists_objects(client):
    """
    Testuje widok listy psów.

    Sprawdza, czy endpoint `dogs` poprawnie zwraca stronę z listą psów,
    a także czy liczba psów w kontekście odpowiada liczbie w bazie.
    """
    DogFactory.create_batch(5)
    url = reverse("dogs")
    res = client.get(url)
    assert res.status_code == 200
    assert "dogs_list" in res.context
    assert res.context["dogs_list"].paginator.count == 5


@pytest.mark.django_db
def test_single_dog_post_creates_review(client):
    """
    Testuje dodawanie recenzji (review) do psa.

    Sprawdza, czy zalogowany użytkownik może dodać recenzję do psa,
    oraz czy obiekt `Review` jest zapisywany w bazie danych.
    """
    # 1) Tworzymy psa wraz z właścicielem i profilem
    dog = DogFactory()

    # 2) Pobieramy istniejącego usera tego samego profilu
    user = dog.owner.user        # owner = Profile, profile.user = User
    client.login(username=user.username, password="pass")   # hasło ustawione w UserFactory

    url = reverse("dog", args=[dog.id])
    data = {"value": "up", "body": "Super!"}
    res = client.post(url, data, follow=True)

    assert res.status_code == 200
    assert Review.objects.filter(owner=dog.owner, dog=dog).exists()
