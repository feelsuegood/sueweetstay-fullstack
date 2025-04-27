import typing
from strawberry.permission import BasePermission
from strawberry.types import Info


class OnlyLoggedIn(BasePermission):

    message = "You need to be logged in for this"

    def has_permission(self, source: typing.Any, info: Info):
        return info.context.request.user.is_authenticated
