from config import settings
import strawberry
import strawberry.django
import typing
from strawberry import auto
from strawberry.types import Info
from reviews.types import ReviewType
from . import models
from users.types import UserType
from wishlists.models import Wishlist


@strawberry.django.type(models.Room)
class RoomType:
    pk: auto = strawberry.django.field(field_name="id")
    name: auto
    kind: auto
    owner: "UserType"

    @strawberry.field
    # * optional typing
    def reviews(self, page: typing.Optional[int] = 1) -> typing.List["ReviewType"]:
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        return self.reviews.all()[start:end]

    @strawberry.field
    def rating(self) -> str:
        return self.rating()

    # * custom methods
    @strawberry.field
    def is_owner(self, info: Info) -> bool:
        return self.owner == info.context.request.user

    @strawberry.field
    def is_liked(self, info: Info) -> bool:
        return Wishlist.objects.filter(
            user=info.context.request.user,
            rooms__pk=self.pk,
        ).exists()
