from rest_framework import serializers
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from users.serializers import TinyUserSerializer
from wishlists.models import Wishlist
from .models import Experience, Perk


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    total_perks = serializers.SerializerMethodField()

    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "total_perks",
            "rating",
            "is_host",
            "photos",
        )

    def get_rating(self, experience):
        experience.rating()

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_total_perks(self, experience):
        return experience.total_perks()


class ExperienceDetailSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(
        read_only=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    total_perks = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        exclude = ("perks",)

    def get_total_perks(self, experience):
        return experience.total_perks()

    def get_rating(self, experience):
        experience.rating()

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user

    def get_is_liked(self, experience):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user,
            experiences__pk=experience.pk,
        ).exists()
