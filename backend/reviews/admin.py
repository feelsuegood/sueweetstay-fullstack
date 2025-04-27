from django.contrib import admin
from .models import Review


# custom filter
class WordFilter(admin.SimpleListFilter):
    title = "Filter by words"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("nice", "Nice"),
            ("very", "Very"),
        ]

    def queryset(self, request, reviews):
        # print(dir(request))
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


class GoodOrBadFilter(admin.SimpleListFilter):
    title = "Filter by good or bad"
    parameter_name = "good-or-bad"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, reviews):
        if self.value() == "good":
            return reviews.filter(rating__gte=3)
        elif self.value() == "bad":
            return reviews.filter(rating__lt=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("__str__", "payload", "room", "experience")

    list_filter = (
        WordFilter,
        GoodOrBadFilter,
        "rating",
        # custom filters
        "user__is_host",
        "room__category",
        "room__pet_friendly",
        # double foreign keys
        "room__owner__username",
    )
