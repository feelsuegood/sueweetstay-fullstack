import time  # for frontend test
from django.db import transaction
from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    ValidationError,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config import settings
from .models import Room, Amenity
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer

# * 'views'.py can be changed to any words


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(AmenitySerializer(new_amenity).data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        # * add ***DoesNotExist***
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):

        serializer = RoomDetailSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'.")
            except Category.DoesNotExist:
                raise ParseError("Category not found.")
            try:
                # Transaction - not commit change immediately, prevent create too many pk
                with transaction.atomic():
                    # foreign key handling
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    # many to many fields handling
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)  # type: ignore

            except Exception:
                raise ParseError("Amenity not found.")

            serializer = RoomDetailSerializer(room)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # for frontend test
        # time.sleep(2)
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        # check user is owner of the room
        if request.user != room.owner:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            if request.data.get("category"):
                try:
                    category_pk = request.data.get("category")
                    # print(category_pk)
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'.")
                except Category.DoesNotExist:
                    raise ParseError("Category Not Found")
            else:
                category = room.category
            try:
                with transaction.atomic():
                    serializer.save(owner=request.user, category=category)
                    if request.data.get("amenities"):
                        amenities = request.data.get("amenities")
                        room.amenities.clear()
                        # print(amenities)
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                    return Response(serializer.data)
            except Exception:
                raise ValidationError

    def delete(self, request, pk):
        room = self.get_object(pk)
        # print(dir(request.user))
        # check user is owner of the room
        if request.user != room.owner:
            raise PermissionDenied
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        ### pagination ###
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        ### pagination ###
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],  # type: ignore
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, room=self.get_object(pk))
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        ### pagination ###
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        ### pagination ###
        room = self.get_object(pk)
        amenities = room.amenities.all()[start:end]
        serializer = AmenitySerializer(
            amenities,
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        # get current date and booking date should be later than current date
        now = timezone.localtime(timezone.now()).date()
        # bookings = Booking.objects.filter(room__pk=pk)
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data, context={"room": room}
        )
        if serializer.is_valid():
            booking = serializer.save(
                kind=Booking.BookingKindChoices.ROOM,
                user=request.user,
                room=room,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class RoomBookingCheck(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    # bookings/check?check_in=date&check_out=date
    def get(self, request, pk):
        room = self.get_object(pk)
        check_out = request.query_params.get("check_out")
        check_out = request.query_params.get("check_in")
        exists = Booking.objects.filter(
            room=room,
            check_in__lte=check_out,
            check_out__gte=check_out,
        ).exists()
        if exists:
            return Response({"ok": False})
        else:
            return Response({"ok": True})


def trigger_error(request: HttpRequest):
    division_by_zero = 1 / 0
    return HttpResponse("This will never be returned")
