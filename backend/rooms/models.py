from django.db import models
from common.models import CommonModel


class Room(CommonModel):
    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(
        max_length=180,
        default="",
    )
    country = models.CharField(
        max_length=50,
        default="Korea",
    )
    city = models.CharField(
        max_length=80,
        default="Seoul",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(
        max_length=250,
    )
    pet_friendly = models.BooleanField(
        default=True,
    )
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        blank=True,
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="rooms",
    )

    def __str__(room) -> str:
        return (room).name

    # ^ same with above
    # def __str__(self) -> str:
    #     return(self).name

    def total_amenities(room):
        return (room).amenities.count()

    def rating(room):
        count = room.reviews.count()  # type: ignore # revers accessor (related_name)
        if count == 0:
            return 0
        else:
            total_rating = 0
            # room.review.all() -> review.rating
            for review in room.reviews.all().values("rating"):  # type: ignore
                total_rating += review["rating"]
            return round(total_rating / count, 2)


class Amenity(CommonModel):
    """Amenity Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
