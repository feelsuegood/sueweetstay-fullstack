import strawberry
import strawberry.django
from strawberry import auto
from strawberry import Info
from . import models
from .types import RoomType
from enum import Enum


@strawberry.enum
class RoomKindInput(Enum):
    ENTIRE_PLACE = "entire_place"
    PRIVATE_ROOM = "private_room"
    SHARE_ROOM = "shared_room"


@strawberry.django.input(models.Room)
class RoomInput:
    name: auto
    country: auto
    city: auto
    price: auto
    rooms: auto
    toilets: auto
    description: auto
    address: auto
    pet_friendly: auto
    kind: RoomKindInput
    amenities: list[int]
    category: int


def add_room(info: Info, input: RoomInput) -> RoomType:
    input_data = {
        key: getattr(input, key)
        for key in input.__annotations__
        if key not in {"amenities", "category", "kind"}
    }

    new_room = models.Room.objects.create(
        **input_data,
        kind=input.kind.value,
        owner=info.context.request.user,
        category_id=input.category,
    )
    new_room.amenities.set(input.amenities)
    return strawberry.django.from_model(new_room, RoomType)
