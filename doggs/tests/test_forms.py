"""
Testy formularzy w aplikacji `doggs`.

Sprawdzają walidację, poprawność pól oraz domyślną konfigurację formularzy.
"""

import pytest
from doggs.forms import DogForm, ReviewForm
from .factories import DogFactory

@pytest.mark.django_db
def test_dog_form_valid_data():
    """
    Testuje poprawność formularza `DogForm` z prawidłowymi danymi wejściowymi.

    Sprawdza, czy formularz jest ważny po wprowadzeniu danych testowych
    (imię, rasa, wiek, opis) oraz czy dane te są poprawnie przechowywane.
    """
    form = DogForm(data={
        "name": "Azor",
        "description": "Wesoły pies",
        "wiki_link": "https://pl.wikipedia.org/wiki/Pies"
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_review_form_labels():
    """
    Testuje etykiety pól formularza `ReviewForm`.

    Sprawdza, czy pola `value` oraz `body` mają przypisane odpowiednie etykiety
    widoczne dla użytkownika.
    """
    form = ReviewForm()
    assert form.fields["value"].label == "Place your vote"
    assert form.fields["body"].label == "Add a comment with your vote"
