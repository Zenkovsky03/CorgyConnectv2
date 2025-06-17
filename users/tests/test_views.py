"""
Testy widoków aplikacji `users`.

Zawiera testy funkcjonalne dla:
- listy profili,
- rejestracji użytkownika,
- logowania użytkownika,
- widoku skrzynki odbiorczej (inbox),
- dodawania umiejętności (skill).
"""
# users/tests/test_views.py
import pytest
import factory
from django.urls import reverse
from users.models import Message, Skill
from .factories import UserFactory, ProfileFactory, MessageFactory



#lista profili
@pytest.mark.django_db
def test_profiles_view_lists_profiles(client):
    """
    Testuje, czy widok `profiles` poprawnie wyświetla listę profili.
    """
    ProfileFactory.create_batch(4, name="Visible")
    res = client.get(reverse("profiles"))

    assert res.context["profiles"].paginator.count == 4




#rejestracja
@pytest.mark.django_db
def test_register_creates_user_and_redirects(client):
    """
    Testuje proces rejestracji – sprawdza utworzenie użytkownika i przekierowanie.
    """
    url = reverse("register")
    data = {
        "first_name": "Ala",
        "email": "ala@example.com",
        "username": "ala",
        "password1": "ComplexPass123!",
        "password2": "ComplexPass123!",
    }
    res = client.post(url, data, follow=True)

    assert res.status_code == 200
    assert res.redirect_chain               # był redirect
    assert res.context["user"].username == "ala"


#logowanie
@pytest.mark.django_db
def test_login_redirects_to_account(client):
    """
    Testuje logowanie użytkownika i poprawne przekierowanie do konta/profili.
    """
    user = UserFactory(password="pass")
    ProfileFactory(user=user)               # zapewniamy profil
    res = client.post(reverse("login"),
                      {"username": user.username, "password": "pass"})
    assert res.status_code == 302
    assert res.url.rstrip("/").endswith(("account", "profiles"))


#inbox
@pytest.mark.django_db
def test_inbox_only_recipient_messages(client):
    """
    Testuje, czy skrzynka odbiorcza pokazuje tylko wiadomości dla zalogowanego odbiorcy.
    """
    recipient = ProfileFactory()
    sender    = ProfileFactory()

    msg_unread = MessageFactory(sender=sender, recipient=recipient, is_read=False)
    MessageFactory(sender=sender, recipient=recipient, is_read=True)
    MessageFactory(sender=sender, recipient=ProfileFactory())

    client.force_login(recipient.user)
    res = client.get(reverse("inbox"))

    assert msg_unread in res.context["messageRequests"]
    assert res.context["unreadMessages"] == 1


#dodawanie skilla
@pytest.mark.django_db
def test_create_skill_post_adds_skill(client):
    """
    Testuje dodawanie nowej umiejętności do profilu przez widok `create-skill`.
    """
    profile = ProfileFactory()              # ma już usera
    client.force_login(profile.user)

    res = client.post(
        reverse("create-skill"),
        {"name": "Docker", "description": "Containerisation"},
        follow=True,
    )

    assert res.status_code == 200
    assert Skill.objects.filter(owner=profile, name="Docker").exists()
