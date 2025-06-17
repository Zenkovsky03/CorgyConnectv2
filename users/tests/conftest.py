"""
Plik konfiguracyjny `conftest.py` dla testów jednostkowych aplikacji Django.

Zawiera fiksturę globalną, która wycisza wysyłanie wiadomości e-mail podczas testów,
aby uniknąć przypadkowego wykonywania rzeczywistej wysyłki e-maili z poziomu sygnałów Django.
"""
import pytest
from unittest.mock import Mock

@pytest.fixture(autouse=True)
def _mute_send_mail(monkeypatch):
    """
    Fikstura automatycznie stosowana do wszystkich testów.

    Zastępuje funkcję `send_mail` w module `users.signals` atrapą (Mock),
    co zapobiega rzeczywistemu wysyłaniu e-maili w czasie testów.
    """
    monkeypatch.setattr("users.signals.send_mail", Mock())
