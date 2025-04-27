from django.utils import timezone
from django.db import models
from common.models import CommonModel


class Experience(CommonModel):
    """Experience Model Definition"""

    name = models.CharField(
        max_length=250,
    )
    country = models.CharField(
        max_length=50,
        default="Australia",
    )
    city = models.CharField(
        max_length=80,
        default="Gold Coast",
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="experiences",
    )

    def __str__(self) -> str:
        return self.name

    def total_perks(experience):
        return experience.perks.count()

    def rating(experience):
        count = experience.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in experience.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)

    def duration(experience):
        today = timezone.localdate()
        start_dt = timezone.datetime.combine(today, experience.start)
        end_dt = timezone.datetime.combine(today, experience.end)
        return end_dt - start_dt


class Perk(CommonModel):
    """What is included on an Experience"""

    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self) -> str:
        return self.name
