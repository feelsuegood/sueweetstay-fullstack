import strawberry
import strawberry.django
from strawberry import auto
from . import models


@strawberry.django.type(models.Review)
class ReviewType:
    pk: auto = strawberry.django.field(field_name="id")
    payload: auto
    rating: auto
