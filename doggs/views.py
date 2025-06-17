"""
Widoki aplikacji `doggs` obsługujące przeglądanie, tworzenie, edycję i usuwanie psów oraz ich recenzji.

Zawiera:
- listę i szczegóły psów
- formularze do recenzji
- widoki do CRUD psów (Create, Read, Update, Delete)
"""

from django.shortcuts import render, redirect
from .models import Dog, Tag
from .forms import DogForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import searchDogs, paginateDogs


import logging
logger = logging.getLogger('doggs')



def dogs(request):
    """
    Widok listy psów z obsługą wyszukiwania i paginacji.

    Zwraca wyniki z funkcji pomocniczych `searchDogs` i `paginateDogs`.

    Returns:
        HttpResponse: wyrenderowana strona z listą psów (`doggs/dogs.html`).
    """
    dogs, search_query = searchDogs(request)
    custom_range, dogs = paginateDogs(request, dogs, 3)
    context = {
        'dogs_list': dogs,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    logger.info("Wyświetlono listę psów.")
    return render(request, 'doggs/dogs.html', context)


def dog(request, pk):
    """
    Wyświetla szczegóły wybranego psa oraz formularz do dodania recenzji.

    Args:
        pk (int): ID psa.

    Returns:
        HttpResponse: strona `doggs/single-dog.html` z informacjami o psie.
    """
    dogObj = Dog.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.dog = dogObj
            review.owner = request.user.profile
            review.save()

            dogObj.getVoteCount
            messages.success(request, 'Your review was successfully submitted.')
            logger.info(f"Otwarto szczegóły psa o ID: {pk}")
            return redirect('dog', pk=dogObj.id)
    context = {
        'dogObj': dogObj,
        'form': form,
    }
    return render(request, 'doggs/single-dog.html', context)

@login_required(login_url='login')
def createDog(request):
    """
    Widok dodawania nowego psa przypisanego do aktualnego użytkownika.

    Returns:
        HttpResponse: formularz `doggs/dog_form.html` lub przekierowanie do konta.
    """
    profile = request.user.profile
    form = DogForm()
    if request.method == 'POST':
        newTags = request.POST.get('newTags').replace(",", " ").split()
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.owner = profile
            dog.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                dog.tags.add(tag)

            logger.info(f"Użytkownik {profile} tworzy nowego psa.")
            return redirect('account')
    context = {
        'form': form,
    }
    return render(request, 'doggs/dog_form.html', context)

@login_required(login_url='login')
def updateDog(request, pk):
    """
    Widok edycji psa należącego do użytkownika.

    Args:
        pk (int): ID psa do edycji.

    Returns:
        HttpResponse: formularz `doggs/dog_form.html` lub redirect do konta.
    """
    profile = request.user.profile
    dogObj = profile.dog_set.get(id=pk)
    form = DogForm(instance=dogObj)
    if request.method == 'POST':
        newTags = request.POST.get('newTags').replace(",", " ").split()
        form = DogForm(request.POST, request.FILES, instance=dogObj)
        if form.is_valid():
            dog = form.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                dog.tags.add(tag)

            logger.info(f"Użytkownik {profile} edytuje psa o ID: {pk}")
            return redirect('dogs')
    context = {
        'form': form,
        'dogObj': dogObj,
    }
    return render(request, 'doggs/dog_form.html', context)

@login_required(login_url='login')
def deleteDog(request, pk):
    """
    Widok usuwania psa (potwierdzenie).

    Args:
        pk (int): ID psa do usunięcia.

    Returns:
        HttpResponse: strona potwierdzenia usunięcia lub redirect po wykonaniu.
    """
    profile = request.user.profile
    dogObj = profile.dog_set.get(id=pk)
    if request.method == 'POST':
        dogObj.delete()
        logger.warning(f"Pies {dogObj.name} został usunięty przez {profile}.")
        return redirect('account')
    context = {
        'object': dogObj
    }
    return render(request, 'delete_object.html', context)
