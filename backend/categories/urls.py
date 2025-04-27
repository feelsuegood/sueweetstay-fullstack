from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.CategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "rooms",
        views.CategoryRoomsViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "experiences",
        views.CategoryExperiencesViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
]
