import random
import urllib.request
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
from faker import Faker

from users.models import Profile, Skill, Message
from doggs.models import Dog, Tag, Review
import uuid
User = get_user_model()
fake = Faker("pl_PL")

# 🧠 LISTY DANYCH

ABOUT_ME_LIST = [
    "Miłośnik psów i długich spacerów po lesie.",
    "Z pasji do zwierząt zostałem behawiorystą.",
    "Na co dzień pomagam ludziom i ich pupilom lepiej się zrozumieć.",
    "Uwielbiam uczyć psy nowych sztuczek i obserwować ich rozwój.",
    "Z psami pracuję od ponad 10 lat — to nie tylko zawód, to styl życia.",
    "Prowadzę szkolenia dla psów i warsztaty dla opiekunów.",
    "Wolne chwile spędzam na łonie natury — najlepiej z psem u boku.",
    "Jestem opiekunem, trenerem i przyjacielem każdego czworonoga.",
    "Zajmuję się opieką dzienną i nocną dla psów.",
    "Pomagam właścicielom rozwiązywać problemy z zachowaniem psów.",
]

SHORT_INTRO_LIST = [
    "Pasja do psów od najmłodszych lat.",
    "Trenerka z doświadczeniem i sercem.",
    "Zawsze blisko zwierząt i natury.",
    "Uczę psy i ich opiekunów z uśmiechem.",
    "Behawiorystka z zamiłowaniem do wyzwań.",
    "Pomagam budować więź człowiek–pies.",
    "Codziennie uczę się czegoś od psów.",
    "Spacery, szkolenia i dobra kawa!",
    "Pies to nie obowiązek — to przyjaciel.",
    "Szczęśliwy pies to spokojny dom.",
]

SKILL_CHOICES = [
    "Tresura obronna", "Dog-trekking", "Agility", "Grooming",
    "Behawiorystyka", "Pierwsza pomoc", "Pet-sitting", "Fotografia psów"
]

SKILL_DESCRIPTIONS = [
    "Prowadzę szkolenia indywidualne i grupowe.",
    "Specjalizuję się w rozwiązywaniu problemów behawioralnych.",
    "Pomagam szczeniakom poznać świat.",
    "Szkolenie dostosowane do potrzeb i charakteru psa.",
    "Uczę podstawowych i zaawansowanych komend.",
    "Opiekuję się psami w domowych warunkach.",
]

DOG_NAMES = [
    "Reksio", "Luna", "Max", "Kora", "Szarik", "Bella", "Figo", "Nero"
]

DOG_DESCRIPTIONS = [
    "Przyjazny i energiczny, idealny towarzysz do biegania.",
    "Spokojny i łagodny, świetny dla rodziny z dziećmi.",
    "Lubi długie spacery i zabawy na świeżym powietrzu.",
    "Ma dobre maniery i zna podstawowe komendy.",
]

REVIEW_COMMENTS = [
    "Świetny pies, bardzo dobrze ułożony!",
    "Zaskoczył mnie pozytywnie, bardzo grzeczny.",
    "Ma cudowny charakter, polecam!",
    "Energiczny i chętny do zabawy.",
    "Bardzo zadbany i przyjazny.",
    "Miły w kontakcie, nie szczeka bez potrzeby.",
    "Widać, że ma dobre relacje z ludźmi.",
    "Sympatyczny i pełen energii.",
    "Jeden z lepszych psów, jakie poznałem.",
    "Spokojny w domu, żywiołowy na spacerach.",
]

TAGS = ["towarzyski", "szkolony", "aktywny", "przyjacielski", "rodzinny", "czujny"]

# 📦 FUNKCJE POMOCNICZE

def fetch_avatar(username):
    try:
        img_id = random.randint(1, 70)  # zakres bezpieczny
        url = f"https://i.pravatar.cc/300?img={img_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            return ContentFile(response.read(), name=f"{username}.jpg")
    except Exception as e:
        print(f"⚠️ Avatar error: {e}")
        return None




def fetch_dog_image():
    try:
        dog_id = random.randint(1, 100)
        url = f"https://placedog.net/640/480?id={dog_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            return ContentFile(response.read(), name=f"dog_{dog_id}.jpg")
    except:
        # fallback – domyślna grafika (musi istnieć w media)
        with open("media/dogs/default.jpg", "rb") as f:
            return ContentFile(f.read(), name="default.jpg")




# 🚀 KOMENDA

class Command(BaseCommand):
    help = "Seed demo data into the database."

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=10)
        parser.add_argument("--dogs-per-user", type=int, default=2)
        parser.add_argument("--skills-per-user", type=int, default=3)
        parser.add_argument("--reviews-per-dog", type=int, default=4)

    def handle(self, *args, **opts):
        users_count = opts["users"]

        self.stdout.write("🧹 Czyszczenie danych...")
        Dog.objects.all().delete()
        Tag.objects.all().delete()
        Review.objects.all().delete()
        Message.objects.all().delete()
        Profile.objects.exclude(user__is_superuser=True).delete()
        User.objects.exclude(is_superuser=True).delete()

        tag_objs = [Tag.objects.get_or_create(name=name)[0] for name in TAGS]
        profiles = []

        for _ in range(users_count):
            username = fake.unique.user_name()
            user = User.objects.create_user(
                username=username,
                email=fake.unique.email(),
                password="pass1234!",
                first_name=fake.first_name(),
            )

            profile = user.profile
            profile.name = user.first_name
            profile.username = username
            profile.email = user.email
            profile.location = fake.city()
            profile.short_intro = random.choice(SHORT_INTRO_LIST)
            profile.bio = random.choice(ABOUT_ME_LIST)

            avatar = fetch_avatar(username)
            if avatar:
                profile.profile_image.save(avatar.name, avatar, save=False)
            profile.save()
            profiles.append(profile)

            # losowe skille 1–5
            for _ in range(random.randint(1, 5)):
                Skill.objects.create(
                    owner=profile,
                    name=random.choice(SKILL_CHOICES),
                    description=random.choice(SKILL_DESCRIPTIONS),
                )

            # losowe psy 1–4
            for _ in range(random.randint(1, 4)):
                dog = Dog.objects.create(
                    owner=profile,
                    name=random.choice(DOG_NAMES),
                    description=random.choice(DOG_DESCRIPTIONS),
                    wiki_link="https://pl.wikipedia.org/wiki/Pies_domowy",
                    created=timezone.now()
                )

                dog_image = fetch_dog_image()
                if dog_image:
                    dog.featured_image.save(dog_image.name, dog_image, save=False)
                dog.save()

                # losowe tagi 1–4
                dog.tags.set(random.sample(tag_objs, k=random.randint(1, 4)))

        for dog in Dog.objects.all():
            reviewers = random.sample(profiles, k=random.randint(1, min(8, len(profiles))))
            for reviewer in reviewers:
                Review.objects.create(
                    owner=reviewer,
                    dog=dog,
                    value=random.choice(["up", "down"]),
                    body=random.choice(REVIEW_COMMENTS),
                )
            dog.getVoteCount  # przelicz głosy po recenzjach

        for _ in range(users_count * 2):
            sender, recipient = random.sample(profiles, 2)
            Message.objects.create(
                sender=sender,
                recipient=recipient,
                subject=fake.sentence(nb_words=4),
                body=fake.paragraph(),
                is_read=random.choice([True, False]),
            )

        self.stdout.write(self.style.SUCCESS("✅ Gotowe! Baza danych została zapełniona."))
