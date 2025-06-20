import random
from django.core.management.base import BaseCommand
from medias.models import Photo
from rooms.models import Room


class Command(BaseCommand):
    help = "Seed 5 random photos per room"

    def handle(self, *args, **kwargs):
        image_urls = [
            "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=900&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=900&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1480074568708-e7b720bb3f09?w=900&auto=format&fit=crop&q=60",
            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=900&auto=format&fit=crop&q=60",
            "https://plus.unsplash.com/premium_photo-1689609950112-d66095626efb?q=80&w=900&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?w=900&auto=format&fit=crop&q=60",
        ]

        rooms = Room.objects.all()

        if not rooms.exists():
            self.stdout.write(
                self.style.ERROR("❌ No rooms found. Run `seed_rooms` first.")
            )
            return

        for idx, room in enumerate(rooms):
            chosen_urls = random.sample(image_urls, 5)  # 5 random choices
            for i, url in enumerate(chosen_urls):
                Photo.objects.create(
                    file=url,
                    description=f"{i + 1} - Photo for {room.name}",
                    room=room,
                )

        self.stdout.write(
            self.style.SUCCESS(f"✅ Seeded 5 photos for each of {rooms.count()} rooms.")
        )
