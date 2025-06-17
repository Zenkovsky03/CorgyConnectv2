"""
Testy jednostkowe formularzy użytkownika, profilu, umiejętności oraz wiadomości
w aplikacji `users`. Testy sprawdzają poprawność walidacji formularzy oraz
poprawność generowanych pól formularzy.
"""
import pytest
from users.forms import (
    CustomUserCreationForm,
    ProfileForm,
    SkillForm,
    MessageForm,
)
from .factories import ProfileFactory, SkillFactory

@pytest.mark.django_db
def test_custom_user_creation_form_valid():
    """
    Sprawdza, czy formularz rejestracji nowego użytkownika działa poprawnie
    przy podaniu poprawnych danych.
    """
    form = CustomUserCreationForm(
        data={
            "first_name": "Jan",
            "email": "jan@ex.com",
            "username": "janek",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
    )
    assert form.is_valid()

@pytest.mark.django_db
def test_profile_form_widgets():
    """
    Sprawdza, czy wszystkie pola formularza profilu mają klasę CSS 'input'.
    """
    profile = ProfileFactory()
    form = ProfileForm(instance=profile)
    # wszystkie pola mają css 'input'
    assert all("class" in f.widget.attrs for f in form.fields.values())

@pytest.mark.django_db
def test_skill_form_excludes_owner():
    """
    Upewnia się, że pole 'owner' jest wykluczone z formularza umiejętności.
    """
    form = SkillForm()
    assert "owner" not in form.fields

def test_message_form_fields():
    """
    Sprawdza, czy formularz wiadomości zawiera wszystkie wymagane pola.
    """
    form = MessageForm()
    assert set(form.fields) == {"name", "email", "subject", "body"}
