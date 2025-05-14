from django.db import transaction
from rest_framework import serializers

from airport.models import (Airport,
                            Route,
                            AirplaneType,
                            Airplane,
                            Crew,
                            Flight,
                            Order,
                            Ticket)


# Views -> Create, List
# Ser -> Write List with same fields
class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")
        read_only_fields = ("id",)


class AirportListSerializer(AirportSerializer):
    pass

# Views -> Create, List
# Ser -> Write List with same fields
class AirplaneTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirplaneType
        fields = ("id", "name",)
        read_only_fields = ("id",)

class AirplaneTypeListSerializer(AirplaneTypeSerializer):
    pass


# Views -> Create, List
# Ser -> Write List with detail info airplane_type, read only
class AirplaneSerializer(serializers.ModelSerializer):

    airplane_type = AirplaneTypeSerializer(many=False, read_only=False)

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "capacity", "airplane_type")
        read_only_fields = ("capacity", "id",)

    def create(self, validated_data):
        with transaction.atomic():
            type_data = validated_data.pop("airplane_type")
            name = type_data.get("name")

            airplane_type = AirplaneType.objects.filter(name__icontains=name).get()
            if not airplane_type:
                airplane_type = AirplaneType.objects.create(name=name)

            return Airplane.objects.create(airplane_type=airplane_type, **validated_data)

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

    airplane_type = AirplaneSerializer(many=True, read_only=True)


# Views -> Create, List
# Ser -> List with (source\destination -> id, name) read only, maybe many
class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")
        read_only_fields = ("id",)


class RouteListSerializer(RouteSerializer):

    source = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    destination = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")


# Views -> Create, List
# Ser -> List with same field
class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")
        read_only_fields = ("id",)


class CrewListSerializer(CrewSerializer):
    pass


# Views -> Create, List, Retrieve
# Ser -> List(try Crew id with comma), Retrieve(Detail information for crew)
class FlightSerializer(serializers.ModelSerializer):


    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")
        read_only_fields = ("id",)


# Views -> CRUD
# Ser -> Created Ticket in order, Order pagination, List(only your order, all detail information with foreign key related)
class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("id", "created_at", "user")
        read_only_fields = ("id",)


# Delete Ticket serializer
class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")
        read_only_fields = ("id",)
