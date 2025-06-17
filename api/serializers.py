"""
Serializery dla aplikacji `doggs`.

Zawierają klasy serializujące modele:
- `Dog` – z uwzględnieniem tagów i oceny,
- `Review` – komentarze i recenzje użytkowników.

Serializery umożliwiają konwersję danych modeli na format JSON i odwrotnie, używany w API.
"""

from rest_framework import serializers
from doggs.models import Dog, Tag, Review
from users.models import Profile

class TagSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu Tag.

    Umożliwia reprezentację tagów przypisanych do psów w formacie JSON.
    Zawiera pola:
    - `name` – nazwa tagu,
    - `created` – data utworzenia.

    Stosowany przy odczycie i zapisie tagów w API.
    """
    class Meta:
        model = Tag
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu Profile użytkownika.

    Służy do serializacji danych użytkownika, takich jak:
    - `name`, `email`, `username`, `location` – dane kontaktowe i identyfikacyjne,
    - `short_intro`, `bio` – opis i notka wprowadzająca,
    - `image` – zdjęcie profilowe,
    - `social_github`, `social_twitter`, `social_linkedin`, `social_website` – linki społecznościowe.

    Umożliwia reprezentację profilu użytkownika w formacie JSON w API.
    """
    class Meta:
        model = Profile
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu Review (komentarze).

    Zawiera podstawowe dane recenzji:
    - `body`, `value` – treść i ocena,
    - `created` – data dodania recenzji.

    Używany przy dodawaniu i wyświetlaniu opinii o psach.
    """
    class Meta:
        model = Review
        exclude = ['dog']


class DogSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu Dog.

    Zawiera wszystkie pola modelu oraz pola obliczeniowe:
    - `tags` – lista tagów przypisanych do psa,
    - `vote_total`, `vote_ratio` – dane statystyczne o ocenach psa.

    Służy do konwersji obiektów Dog na JSON w REST API.
    """
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Dog
        fields = '__all__'


    def get_reviews(self, obj):
        """
        Zwraca listę recenzji powiązanych z aktualnie zalogowanym użytkownikiem.

        Zwraca dane w formacie JSON, zawierające:
        - identyfikator recenzji,
        - powiązanego psa,
        - treść i ocenę recenzji.

        Wymaga uwierzytelnienia tokenem JWT.
        """
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data




