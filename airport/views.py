from rest_framework import viewsets, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet

from airport.models import (Airplane,
                            AirplaneType,
                            Airport,
                            Route,
                            Crew,
                            Flight,
                            Order,
                            Ticket)
from airport.serializers import (AirplaneSerializer,
                                 AirplaneTypeSerializer,
                                 AirportSerializer,
                                 RouteSerializer,
                                 CrewSerializer,
                                 FlightSerializer,
                                 OrderSerializer,
                                 TicketSerializer, AirplaneListSerializer, RouteListSerializer, FlightDetailSerializer,
                                 FlightListSerializer)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly

class CreateListOperation(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    pass


class AirplaneViewSet(CreateListOperation):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return AirplaneSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.select_related()
        return queryset


class AirplaneTypeViewSet(CreateListOperation):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]



class AirportViewSet(CreateListOperation):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]


class RouteViewSet(CreateListOperation):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.select_related()
        return queryset


class CrewViewSet(CreateListOperation):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]



class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in {"list", "retrieve"}:
            return queryset.prefetch_related()
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]