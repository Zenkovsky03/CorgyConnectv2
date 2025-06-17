import pytest
from doggs.models import Dog, Review, Tag
from .factories import DogFactory, ReviewFactory, TagFactory

@pytest.mark.django_db
def test_str_methods():
    """
    Testuje metodę __str__ modeli Dog, Tag i Review.
    Sprawdza, czy zwracają poprawne reprezentacje tekstowe.
    """
    dog = DogFactory(name="Azor")
    tag = TagFactory(name="mały")
    review = ReviewFactory(value="up")
    assert str(dog) == "Azor"
    assert str(tag) == "mały"
    assert str(review) == "up"

@pytest.mark.django_db
def test_dog_vote_count_computes_ratio():
    """
    Testuje poprawność obliczania liczby głosów i stosunku głosów w modelu Dog.
    Trzy głosy pozytywne i jeden negatywny powinny dać łącznie 4 głosy i stosunek 75%.
    """
    dog = DogFactory()
    ReviewFactory.create_batch(3, dog=dog, value="up")
    ReviewFactory.create_batch(1, dog=dog, value="down")
    dog.getVoteCount              # property zapisuje się samo
    dog.refresh_from_db()
    assert dog.vote_total == 4
    assert dog.vote_ratio == 75   # 3/4 * 100

@pytest.mark.django_db
def test_review_unique_together_enforced():
    """
    Testuje unikalność opinii (Review) dla danego właściciela i psa.
    Próba dodania drugiej opinii tego samego właściciela dla tego samego psa powinna rzucić wyjątek.
    """
    review = ReviewFactory()
    with pytest.raises(Exception):
      # drugi review tego samego właściciela dla tego psa → błąd
      ReviewFactory(owner=review.owner, dog=review.dog)
