import strawberry
import strawberry.django
from strawberry import auto
from enum import Enum
from . import models


@strawberry.enum
class CategoryKindChoices(Enum):
    ROOMS = "rooms"
    EXPERIENCES = "experiences"


@strawberry.django.type(model=models.Category)
class CategoryType:
    name: auto
    kind: CategoryKindChoices
