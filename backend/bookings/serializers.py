from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from .models import Booking
from experiences.models import Experience


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    # start - end = duration
    # for duration, it can be used when user try to book other experience in overlapped time with a booked experience

    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests",
        )

    # it's okay there are several groups in experiences
    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        if value.time() != self.context["experience"].start:
            raise serializers.ValidationError(
                "The booking start time must be the same as experience start time"
            )
        return timezone.localtime(value)

    def validate_guests(self, value):
        max = 5
        if max < value:
            raise serializers.ValidationError("This exceeds the maximum guest limit")
        else:
            return value


# create data
class CreateRoomBookingSerializer(serializers.ModelSerializer):

    # required by default
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        else:
            return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        else:
            return value

    def validate(self, data):
        room = self.context.get("room")
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check-out date must be later than the check-in date."
            )
        # Can't cover overlapped parts -> check_in__gte=data["check_in"], check_out__lte=data["check_out"],
        if Booking.objects.filter(
            room=room,
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (some) of dates are already Booked"
            )
        return data


# display data
class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
