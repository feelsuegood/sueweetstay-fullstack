import strawberry
import typing
import strawberry.django
from . import types
from . import queries
from . import mutations
from common.permissions import OnlyLoggedIn


@strawberry.type
class Query:
    all_rooms: typing.List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms, permission_classes=[OnlyLoggedIn]
    )
    # nullable
    room: typing.Optional[types.RoomType] = strawberry.field(resolver=queries.get_room)


@strawberry.type
class Mutation:
    add_room: types.RoomType = strawberry.field(resolver=mutations.add_room)
