"""
Widoki API aplikacji `doggs`.

Zawiera endpointy REST API pozwalające na:
- pobranie listy psów (`getDogs`),
- pobranie konkretnego psa (`getDog`),
- głosowanie na psa (`dogVote`),
- usuwanie tagów (`removeTag`),
- oraz listę tras API (`getRoutes`).

Wymaga autoryzacji dla operacji modyfikujących dane.
"""
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import DogSerializer
from doggs.models import Dog, Review, Tag
@api_view(['GET'])
def getRoutes(request):
    """
    Zwraca listę dostępnych endpoints API.

    :param request: Obiekt żądania HTTP
    :return: Response – lista tras
    """
    routes = [
        {'GET':'/api/dogs'},
        {'GET': '/api/dogs/id'},
        {'POST': '/api/dogs/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},

    ]

    return Response(routes)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getDogs(request):
    """
    Zwraca listę wszystkich psów w systemie.

    :param request: Obiekt żądania HTTP
    :return: Response – serializowana lista psów
    """
    dogs = Dog.objects.all()
    serializer = DogSerializer(dogs, many=True) #many=True to znaczy ze wiele obiektow a nie tylko jeden
    return Response(serializer.data)


@api_view(['GET'])
def getDog(request, pk):
    """
    Zwraca szczegóły konkretnego psa.

    :param request: Obiekt żądania HTTP
    :param pk: ID psa
    :return: Response – dane psa
    """
    dog = Dog.objects.get(id=pk)
    serializer = DogSerializer(dog, many=False) #many=True to znaczy ze wiele obiektow a nie tylko jeden
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dogVote(request, pk):
    """
    Dodaje lub aktualizuje ocenę psa.

    :param request: Obiekt żądania HTTP zawierający dane oceny
    :param pk: ID psa
    :return: Response – serializowane dane psa po aktualizacji
    """
    dog = Dog.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    review, created = Review.objects.get_or_create(
        owner=user,
        dog=dog,
    )
    # czy istnieje recenzja w bazie danych, której właścicielem jest określony użytkownik dla określonego psa.
    # Jeśli taka recenzja już istnieje, jest ona pobierana. Jeśli nie istnieje, jest tworzona nowa recenzja.
    # Zmienna created informuje nas, czy recenzja została utworzona podczas tej operacji czy nie
    review.value = data['value']
    review.save()
    dog.getVoteCount
    serializer = DogSerializer(dog, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request): #usunac tag z danego obiektu a nie usunac ogolnie
    """
    Usuwa tag przypisany do psa.

    :param request: Obiekt żądania HTTP z ID tagu i psa
    :return: Response – komunikat o sukcesie
    """
    tagID = request.data['tag']
    dogID = request.data['dog']

    dog = Dog.objects.get(id=dogID)
    tag = Tag.objects.get(id=tagID)

    dog.tags.remove(tag)
    return Response("Tag was deleted!!!")