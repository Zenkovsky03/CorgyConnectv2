"""
Modele aplikacji `doggs`.

Zawiera:
- `Dog`: reprezentuje psa przypisanego do użytkownika
- `Review`: recenzje psów wraz z głosami
- `Tag`: tagi (cechy) przypisane do psów
"""

import uuid
from users.models import Profile

from django.db import models

class Dog(models.Model):
    """
    Model reprezentujący psa.

    Atrybuty:
        owner (Profile): właściciel psa.
        title (str): nazwa psa.
        description (str): opis.
        featured_image (Image): zdjęcie.
        demo_link, source_link (str): linki.
        tags (Tag): tagi powiązane z psem.
        vote_total, vote_ratio (int): dane głosów.
        created (datetime): data utworzenia.
    """
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    wiki_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'name']

    @property
    def imageURL(self):
        try:
            url= self.featured_image.url
        except:
            url = " "
        return url
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100

        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

class Review(models.Model):
    """
    Model recenzji psa.

    Atrybuty:
        owner (Profile): recenzent.
        dog (Dog): recenzowany pies.
        body (str): treść recenzji.
        value (str): głos ("up" lub "down").
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    owner = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    VOTE_TYPE = (
        ('up', 'Up vote'),
        ('down', 'Down vote')
    )
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['owner', 'dog']]


    def __str__(self):
        return self.value


class Tag(models.Model):
    """
    Model tagów (cech) przypisanych do psów.

    Atrybuty:
        name (str): nazwa tagu.
        created (datetime): czas utworzenia.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
