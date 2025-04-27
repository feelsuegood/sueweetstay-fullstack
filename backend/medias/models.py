from django.db import models
from common.models import CommonModel


class Photo(CommonModel):

    # ! putting an untrusted file in the same location with code is bad
    # file = models.ImageField()
    file = models.URLField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self):
        return f"Photo File for {self.room}"


class Video(CommonModel):
    # ! putting an untrusted file in the same location with code is bad
    # file = models.FileField()
    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="video",
    )

    def __str__(self):
        return "Video File"
