"""
Widoki aplikacji `users` odpowiadające za rejestrację, logowanie, edycję konta,
zarządzanie profilem użytkownika oraz system wiadomości.

Zawiera logikę dla:
- uwierzytelniania i konta użytkownika
- listy i szczegółów profili
- edycji i usuwania umiejętności
- komunikacji między użytkownikami
"""

from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles


import logging
logger = logging.getLogger('users')

def loginUser(request):
    """
    Obsługuje logikę logowania użytkownika.

    Jeśli użytkownik jest już zalogowany — przekierowuje na stronę profilu.
    Jeśli metoda to POST, próbuje uwierzytelnić użytkownika na podstawie loginu i hasła.

    Args:
        request (HttpRequest): żądanie HTTP z danymi logowania.

    Returns:
        HttpResponse: przekierowanie do profilu lub ponowne wyświetlenie formularza logowania.
    """
    page = 'login'

    if request.user.is_authenticated:
        logger.debug(f"[loginUser] {request.user.username} już zalogowany – redirect na profiles")
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        logger.debug(f"[loginUser] Próba logowania: username={username}")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            logger.warning(f"[loginUser] Nieistniejący username: {username}")
            messages.error(request, "Username doesn't exist")
            return render(request, 'users/login_register.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"[loginUser] Pomyślne logowanie dla: {username}")
            return redirect(request.GET.get('next', 'account'))
        else:
            logger.warning(f"[loginUser] Błędne hasło dla: {username}")
            messages.error(request, "Username or password is incorrect")

    return render(request, 'users/login_register.html')




def logoutUser(request):
    """
    Wylogowuje użytkownika i przekierowuje na stronę logowania.

    Args:
        request (HttpRequest): bieżące żądanie użytkownika.

    Returns:
        HttpResponse: przekierowanie do logowania.
    """
    logger.info(f"Użytkownik {request.user} wylogował się.")
    logout(request)
    messages.info(request, "User was logout successfully")
    return redirect('login')

def profiles(request):
    """
    Wyświetla listę wszystkich profili użytkowników.

    Umożliwia przeglądanie kont innych użytkowników. Może być filtrowane
    przez wyszukiwarkę (GET parametr 'q').

    Args:
        request (HttpRequest): żądanie HTTP, potencjalnie zawierające parametr 'q'.

    Returns:
        HttpResponse: strona z listą profili użytkowników.
    """
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'users/profiles.html', context)

def registerUser(request):
    """
    Rejestruje nowego użytkownika w systemie.

    Obsługuje formularz rejestracji i automatycznie loguje użytkownika po poprawnym utworzeniu konta.

    Args:
        request (HttpRequest): żądanie HTTP z danymi rejestracyjnymi.

    Returns:
        HttpResponse: przekierowanie do edycji konta lub ponowne wyświetlenie formularza rejestracji.
    """
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # obiekt jeszcze nie jest zapisany do bazy ale jest do manipulowania typu zmiana wszystkich liter na male
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User Account was created successfully")
            login(request, user)
            logger.info(f"Zarejestrowano nowego użytkownika: {user.username}")
            return redirect('edit-account')
        else:
            messages.error(request,"An error has occurred during registration")
    context = {
        'page':page,
        'form':form,
    }
    return render(request, 'users/login_register.html', context)

def userProfile(request, pk):
    """
    Wyświetla profil konkretnego użytkownika.

    Args:
        request (HttpRequest): żądanie HTTP.
        pk (int): ID profilu do wyświetlenia.

    Returns:
        HttpResponse: strona z profilem użytkownika i jego umiejętnościami.
    """
    profile = Profile.objects.get(id=pk)
    topSKills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {
        'profile': profile,
        'topSkills':topSKills,
        'otherSkills':otherSkills,
    }
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    """
    Wyświetla panel użytkownika z jego profilem, umiejętnościami i wiadomościami.

    Tylko dla użytkownika aktualnie zalogowanego.

    Args:
        request (HttpRequest): żądanie HTTP użytkownika.

    Returns:
        HttpResponse: strona konta użytkownika.
    """
    profile = request.user.profile
    skills = profile.skill_set.all()
    dogs = profile.dog_set.all()
    context = {
        'profile': profile,
        'skills': skills,
        'dogs':dogs,
    }
    logger.info(f"Wyświetlono konto użytkownika: {profile}")
    return render(request, 'users/account.html', context)
@login_required(login_url='login')
def editAccount(request):
    """
    Edycja danych profilu aktualnie zalogowanego użytkownika.

    Args:
        request (HttpRequest): żądanie HTTP z formularzem edycji profilu.

    Returns:
        HttpResponse: formularz edycji profilu lub przekierowanie po zapisaniu.
    """
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'form': form,
    }
    return render(request, 'users/profile-form.html', context)

@login_required(login_url='login')
def createSkill(request):
    """
    Tworzy nową umiejętność i przypisuje ją do profilu aktualnie zalogowanego użytkownika.

    Obsługuje formularz dodawania umiejętności. Po zapisaniu przekierowuje na stronę konta użytkownika.

    Args:
        request (HttpRequest): żądanie HTTP z danymi formularza.

    Returns:
        HttpResponse: przekierowanie do konta użytkownika lub ponowne wyświetlenie formularza z błędami.
    """
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')
    context = {
        'form': form,
    }
    return render(request, 'users/skill-form.html', context)

def updateSkill(request, pk):
    """
    Pozwala edytować istniejącą umiejętność użytkownika.

    Args:
        request (HttpRequest): żądanie HTTP z formularzem.
        pk (int): ID umiejętności do edycji.

    Returns:
        HttpResponse: przekierowanie do konta użytkownika.
    """
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')
    context = {
        'form': form,
    }
    return render(request, 'users/skill-form.html', context)
@login_required(login_url='login')
def deleteSkill(request, pk):
    """
    Usuwa wskazaną umiejętność użytkownika po potwierdzeniu.

    Args:
        request (HttpRequest): żądanie HTTP (POST) z potwierdzeniem.
        pk (int): ID umiejętności do usunięcia.

    Returns:
        HttpResponse: przekierowanie do konta użytkownika.
    """
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')
    context = {
        'object': skill,
    }
    return render(request, 'delete_object.html', context)
@login_required(login_url='login')
def inbox(request):
    """
    Wyświetla skrzynkę odbiorczą zalogowanego użytkownika z otrzymanymi wiadomościami.

    Args:
        request (HttpRequest): żądanie HTTP.

    Returns:
        HttpResponse: strona skrzynki odbiorczej.
    """
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadMessages = messageRequests.filter(is_read=False).count()
    context = {
        'messageRequests': messageRequests,
        'unreadMessages': unreadMessages,
    }
    return render(request, 'users/inbox.html', context)
@login_required(login_url='login')
def viewMessage(request, pk):
    """
    Wyświetla konkretną wiadomość otrzymaną przez użytkownika.

    Zaznacza wiadomość jako przeczytaną, jeśli nie była wcześniej otwarta.

    Args:
        request (HttpRequest): żądanie HTTP.
        pk (int): ID wiadomości do wyświetlenia.

    Returns:
        HttpResponse: strona z treścią wiadomości.
    """
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {
        'message': message,
    }
    return render(request, 'users/message.html', context)

def createMessage(request, pk):
    """
       Pozwala użytkownikowi wysłać wiadomość do innego użytkownika.

       Obsługuje zarówno zalogowanych, jak i niezalogowanych użytkowników.

       Args:
           request (HttpRequest): żądanie HTTP z formularzem.
           pk (int): ID profilu odbiorcy.

       Returns:
           HttpResponse: przekierowanie do profilu odbiorcy po wysłaniu wiadomości.
       """
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # sender = none
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was sent successfully!')
            return redirect('user-profile', pk=recipient.id)
    context = {
        'recipient': recipient,
        'form': form,
    }
    return render(request, 'users/message-form.html', context)
