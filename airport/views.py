from rest_framework import viewsets

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
                                 TicketSerializer)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly,]