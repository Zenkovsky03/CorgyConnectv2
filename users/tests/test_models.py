"""
Moduł testujący modele aplikacji `users`.

Zawiera testy jednostkowe dla modeli: `Profile`, `Skill` oraz `Message`,
w tym metody __str__ oraz właściwości imageURL i porządkowanie wiadomości.
"""
import pytest
from users.models import Message
from .factories import ProfileFactory, SkillFactory, MessageFactory

@pytest.mark.django_db
def test_str_and_image_url():
    """
    Testuje metodę __str__ oraz właściwość `imageURL` w modelach Profile, Skill i Message.
    """
    profile = ProfileFactory()
    assert str(profile) == profile.user.username
    # domyślne zdjęcie → property nie rzuca wyjątku
    assert profile.imageURL.strip() != None

    skill = SkillFactory(name="Python")
    assert str(skill) == "Python"

    msg = MessageFactory(subject="Hi!")
    assert str(msg) == "Hi!"

@pytest.mark.django_db
def test_message_ordering():
    """
    Testuje porządkowanie wiadomości (Message) według pól `is_read` i `created`.
    Wiadomości nieprzeczytane powinny być wyświetlane przed przeczytanymi.
    """
    p1, p2 = ProfileFactory(), ProfileFactory()
    # najpierw przeczytana stara, potem nieprzeczytana nowa → ordering = ['is_read','-created']
    m1 = MessageFactory(sender=p1, recipient=p2, is_read=True)
    m2 = MessageFactory(sender=p1, recipient=p2, is_read=False)
    assert list(Message.objects.all()) == [m2, m1]
