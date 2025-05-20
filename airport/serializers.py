from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket,
)


class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city", "image")
        read_only_fields = ("id",)


class AirportListSerializer(AirportSerializer):

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city", "image")
        read_only_fields = ("id",)


class AirplaneTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirplaneType
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("id",)


class AirplaneSerializer(serializers.ModelSerializer):

    airplane_type = AirplaneTypeSerializer(many=False, read_only=False)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "image",
            "airplane_type",
        )
        read_only_fields = (
            "capacity",
            "id",
        )

    def create(self, validated_data):
        with transaction.atomic():
            type_data = validated_data.pop("airplane_type")
            name = type_data.get("name")

            airplane_type = AirplaneType.objects.filter(name__icontains=name).get()
            if not airplane_type:
                airplane_type = AirplaneType.objects.create(name=name)

            return Airplane.objects.create(
                airplane_type=airplane_type, **validated_data
            )

    def update(self, instance, validated_data):
        with transaction.atomic():
            type_data = validated_data.pop("airplane_type", None)

            if type_data:
                name = type_data.get("name")
                airplane_type = AirplaneType.objects.filter(name__icontains=name).get()
                if not airplane_type:
                    airplane_type = AirplaneType.objects.create(name=name)
                instance.airplane_type = airplane_type

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            return instance


class AirplaneListSerializer(AirplaneSerializer):

    airplane_type = AirplaneTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "airplane_type",
            "image",
        )
        read_only_fields = (
            "capacity",
            "id",
        )


class AirplaneShortListSerializer(AirplaneSerializer):

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "capacity",
        )


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")
        read_only_fields = ("id",)


class RouteListSerializer(RouteSerializer):

    source = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    destination = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")
        read_only_fields = ("id",)


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")
        read_only_fields = ("id",)


class FlightListSerializer(FlightSerializer):

    route = RouteListSerializer(many=False, read_only=True)
    airplane = AirplaneShortListSerializer(many=False, read_only=True)
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )


class FlightDetailSerializer(FlightListSerializer):

    crew = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")
        read_only_fields = ("id", "crew")


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        flight = attrs["flight"]
        row = attrs["row"]
        seat = attrs["seat"]
        Ticket.validate_row(flight, row)
        Ticket.validate_seat(flight, seat, row)

        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")
        read_only_fields = ("id",)


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(many=False, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "ticket")
        read_only_fields = ("id",)


class OrderListSerializer(OrderSerializer):
    ticket = TicketListSerializer(many=False, read_only=True)
