import random
from django.core.management.base import BaseCommand
from rooms.models import Room
from users.models import User  # for owner
from django.utils import timezone


class Command(BaseCommand):
    help = "Seed 20 Room entries"

    def handle(self, *args, **kwargs):
        if not User.objects.exists():
            self.stdout.write(
                self.style.ERROR("No users found. Please create a user first.")
            )
            return

        owner = User.objects.first()  # first user is owner

        cities = ["Gold Coast", "Brisbane", "Sydney", "Melbourne"]
        kinds = ["entire_place", "private_room", "shared_room"]

        for i in range(20):
            Room.objects.create(
                name=f"Test House {i+1}",
                country="Australia",
                city=random.choice(cities),
                price=random.randint(100, 400),
                rooms=random.randint(1, 5),
                toilets=random.randint(1, 3),
                description="Auto-generated test house for development.",
                address=f"{random.randint(1, 100)} Test Street",
                pet_friendly=bool(random.getrandbits(1)),
                kind=random.choice(kinds),
                owner=owner,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded 20 rooms."))
