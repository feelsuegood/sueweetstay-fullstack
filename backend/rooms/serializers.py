from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Room, Amenity
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "pk",
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(
        read_only=True,
    )
    # separated to rooms/1/amenities
    # amenities = AmenitySerializer(
    #     read_only=True,
    #     many=True,
    # )
    category = CategorySerializer(
        read_only=True,
    )
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    total_amenities = SerializerMethodField()
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()
    # ! could kill the database because it loads too many data at once
    # reviews = ReviewSerializer(
    #     many=True,
    #     read_only=True,
    # )

    class Meta:
        model = Room
        exclude = ("amenities",)
        depth = 1

    def get_total_amenities(self, room):
        return room.total_amenities()

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context.get("request")
        if request:
            return room.owner == request.user
        else:
            return False

    def get_is_liked(self, room):
        request = self.context.get("request")
        if request:
            # * many to many field: filter wishlists created by current user and current room
            # https://docs.djangoproject.com/en/5.2/topics/db/examples/many_to_many/
            # "rooms" not room
            if request.user.is_authenticated:
                return Wishlist.objects.filter(
                    user=request.user,
                    rooms__pk=room.pk,
                ).exists()
        else:
            return False

    # * create function automatically called when serializer.save() is called in BTS
    # def create(self, validated_data):
    #     return Room.objects.create(**validated_data)

    # * test code to prevent create a room
    # def create(self, validated_data):
    #     # print(validated_data)
    #     return


class RoomListSerializer(ModelSerializer):

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    total_amenities = SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "city",
            "country",
            "price",
            "rating",
            "is_owner",
            "photos",
            "total_amenities",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_total_amenities(self, room):
        return room.total_amenities()
