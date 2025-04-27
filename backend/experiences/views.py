from functools import partial
from django.utils import timezone
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    ValidationError,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from bookings.serializers import PublicBookingSerializer
from categories.models import Category
from config import settings
from medias.models import Photo
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from .models import Experience, Perk
from . import serializers
from bookings.models import Booking
from bookings.serializers import CreateExperienceBookingSerializer


class Perks(APIView):

    def get(self, request):
        all_perks = Perk.objects.all()
        ### Don't forget "many = True" ###
        serializer = serializers.PerkSerializer(
            all_perks,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            new_perk = serializer.save()
            return Response(serializers.PerkSerializer(new_perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class Experiences(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(
            all_experiences,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            # category validation
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("Category kind should be 'Experiences'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    experience = serializer.save(
                        category=category,
                        host=request.user,
                    )
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
            except:
                raise ParseError("Perk not found")
            serializer = serializers.ExperienceDetailSerializer(experience)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExeprienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            if request.data.get("category"):
                try:
                    category_pk = request.data.get("category")
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("The category kine should be 'Experience'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
            else:
                category = experience.category
            try:
                with transaction.atomic():
                    serializer.save(
                        host=request.user,
                        category=category,
                    )
                    if request.data.get("perks"):
                        perks = request.data.get("perks")
                        experience.perks.clear()
                        for perk_pk in perks:
                            try:
                                perk = Perk.objects.get(pk=perk_pk)
                                experience.perks.add(perk)
                            except Perk.DoesNotExist:
                                raise ParseError(f"Perk with pk {perk_pk} not found")
                    return Response(serializer.data)
            except Exception as e:
                raise ValidationError(f"error{str(e)}")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        experience = self.get_object(pk)
        perks = experience.perks.all()[start:end]
        print(perks)
        serializer = serializers.PerkSerializer(
            perks,
            many=True,
        )
        return Response(serializer.data)


class ExperienceReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        experience = self.get_object(pk)
        serializer = ReviewSerializer(
            experience.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, experience=experience)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperiencePhotos(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(experience=experience)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now())

        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gt=now,
        )
        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(
            data=request.data,
            context={"experience": experience},
        )
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                user=request.user,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get_booking(self, booking_pk):
        try:
            return Booking.objects.get(pk=booking_pk)
        except Booking.DoesNotExist:
            raise NotFound

    def get(self, request, pk, booking_pk):
        experience = self.get_experience(pk)
        booking = self.get_booking(booking_pk)
        serializer = PublicBookingSerializer()
        return Response(serializer.data)

    def put(self, request, pk, booking_pk):
        experience = self.get_experience(pk)
        booking = self.get_booking(booking_pk)
        serializer = CreateExperienceBookingSerializer(
            booking,
            data=request.data,
            partial=True,
            context={"experience": experience},
        )
        if serializer.is_valid():
            booking = serializer.save()
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        if booking.user != request.user:
            raise PermissionDenied
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
