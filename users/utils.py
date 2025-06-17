"""
Funkcje pomocnicze dla aplikacji `users`.

Zawiera:
- `paginateProfiles`: funkcja do dzielenia listy profili na strony i wyliczania zakresu do paginacji.
"""

from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
def searchProfiles(request):
    """
    Wyszukuje profile użytkowników na podstawie zapytania GET (?q=...).

    Args:
        request (HttpRequest): żądanie zawierające parametr 'q'.

    Returns:
        Tuple (QuerySet, str): lista znalezionych profili oraz wartość zapytania.
    """
    search_query = ''
    response = request.GET.get('search_query')
    if response:
        search_query = response
    print("ZNALEZIONO ", search_query)
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)

    )
    return profiles, search_query

def paginateProfiles(request, profiles, results):
    """
    Paginacja listy profili użytkowników

    Obsługuje błędy numeracji stron (np. brak strony, numer spoza zakresu),
    oraz zwraca zakres do wyświetlenia w paginacji (np. 1–10).

    Args:
        request (HttpRequest): Żądanie HTTP z potencjalnym parametrem 'page'.
        profiles (QuerySet): Lista profili do podziału na strony.
        results (int): Liczba profili na jedną stronę.

    Returns:
        Tuple (range, Page): Zakres paginacji (dla przycisków) oraz obiekty z aktualnej strony.
    """
    page = request.GET.get('page') #ktora strona
    # results = 3 #ile obiektow na stronie
    paginator = Paginator(profiles, results) # wywolanie
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger: #jesli np nie podamy zadnej strony albo wartosc ujemna etc
        page = 1
        profiles = paginator.page(page)
    except EmptyPage: #jesli wychodzi poza zakres stron
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles