from django.urls import path, include
from rest_framework import routers

from airport.views import (AirportViewSet,
                           AirplaneViewSet,
                           AirplaneTypeViewSet,
                           RouteViewSet,
                           CrewViewSet,
                           FlightViewSet,
                           OrderViewSet,
                           TicketViewSet)


router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airplanes_type", AirplaneTypeViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
