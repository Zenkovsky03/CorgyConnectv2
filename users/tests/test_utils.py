"""
Testy jednostkowe dla modułu utils w aplikacji users.

Testowane funkcje:
- searchProfiles: przeszukiwanie profili użytkowników na podstawie zapytania.
- paginateProfiles: paginacja wyników wyszukiwania profili.

Wykorzystywane są fabryki ProfileFactory i SkillFactory do generowania danych testowych.
"""
import pytest
from django.test.client import RequestFactory
from users.utils import searchProfiles, paginateProfiles
from .factories import ProfileFactory, SkillFactory

@pytest.mark.django_db
def test_search_profiles_matches_name_and_skill():
    """
    Testuje, czy funkcja searchProfiles poprawnie filtruje profile
    na podstawie umiejętności powiązanych z zapytaniem wyszukiwania.

    Sprawdza, że profil z pasującą umiejętnością jest zwracany,
    a profil niepasujący nie znajduje się w wynikach.
    """
    prof_ok = ProfileFactory()
    prof_ok.name = "Django Ninja"
    prof_ok.save()
    # skill pasujący do zapytania
    SkillFactory(owner=prof_ok, name="python")

    ProfileFactory(name="Nothing")  # nie powinien się znaleźć

    rf = RequestFactory()
    req = rf.get("/profiles", {"search_query": "python"})
    result, q = searchProfiles(req)

    assert prof_ok in result
    assert q == "python"
    assert result.count() == 1

@pytest.mark.django_db
def test_paginate_profiles_basic():
    """
    Testuje podstawowe działanie paginacji profili.

    Tworzy 10 profili i testuje, czy funkcja paginateProfiles poprawnie
    zwraca stronę 2 z 3 obiektami na stronę oraz zakres stron nawigacji.
    """
    # 10 profili, strona 2, po 3 na stronę
    for _ in range(10):
        ProfileFactory()

    rf = RequestFactory()
    req = rf.get("/profiles", {"page": "2"})
    all_profiles, _ = searchProfiles(req)      # bez filtra
    custom_range, page_obj = paginateProfiles(req, all_profiles, 3)

    assert page_obj.number == 2
    assert len(page_obj.object_list) == 3
    # custom_range zawiera okolice bieżącej strony
    assert page_obj.number in custom_range
