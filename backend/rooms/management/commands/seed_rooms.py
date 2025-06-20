import random
from django.core.management.base import BaseCommand
from rooms.models import Room
from users.models import User  # for owner
from django.utils import timezone


class Command(BaseCommand):
    help = "Seed 19 Room entries"

    def handle(self, *args, **kwargs):
        if not User.objects.exists():
            self.stdout.write(
                self.style.ERROR("No users found. Please create a user first.")
            )
            return

        owner = User.objects.first()  # first user is owner

        cities = ["Gold Coast", "Brisbane", "Sydney", "Melbourne"]
        kinds = ["entire_place", "private_room", "shared_room"]

        room_names = [
            "Cozy Beachside Bungalow",
            "Modern City Loft",
            "Serenity Garden Retreat",
            "Sunny Coast Hideaway",
            "Luxury Riverside Villa",
            "Charming Countryside Cottage",
            "Ocean Breeze Studio",
            "Rustic Mountain Cabin",
            "Elegant Urban Apartment",
            "Minimalist Designer Flat",
            "Palm Tree Paradise",
            "Vintage Charm House",
            "Bright Beach Retreat",
            "Tranquil Hillside Haven",
            "Contemporary Family Home",
            "Seaside Serenity Suite",
            "Boho Chic Escape",
            "Tropical Oasis Retreat",
            "Spacious Poolside Villa",
        ]

        for i in range(19):
            Room.objects.create(
                name=room_names[i],
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

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded 19 rooms."))
