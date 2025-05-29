from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from datetime import timedelta

from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Route,
    Crew,
    Flight,
    Order,
    Ticket,
)
from airport.serializers import (
    AirportSerializer,
    AirplaneSerializer,
    FlightSerializer,
    TicketSerializer,
)

AIRPORTS_URL = reverse("airport:airport-list")
AIRPLANES_URL = reverse("airport:airplane-list")
FLIGHTS_URL = reverse("airport:flight-list")
ORDERS_URL = reverse("airport:order-list")
TICKETS_URL = reverse("airport:ticket-list")


def sample_airport(**params):
    defaults = {"name": "Test Airport", "closest_big_city": "Test City"}
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {"name": "Test Type"}
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()
    defaults = {
        "name": "Test Airplane",
        "rows": 30,
        "seats_in_row": 6,
        "airplane_type": airplane_type,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_route(**params):
    source = sample_airport(name="Source Airport")
    destination = sample_airport(name="Destination Airport")
    defaults = {"source": source, "destination": destination, "distance": 1000}
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_crew(**params):
    defaults = {"first_name": "Test", "last_name": "Crew"}
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()
    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": timezone.now() + timedelta(days=1),
        "arrival_time": timezone.now() + timedelta(days=1, hours=2),
    }
    defaults.update(params)
    flight = Flight.objects.create(**defaults)
    crew = sample_crew()
    flight.crew.add(crew)
    return flight


class PublicAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(AIRPORTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@test.com", "testpass")
        self.client.force_authenticate(self.user)

    def test_list_airports(self):
        sample_airport()
        sample_airport(name="Test Airport 2")

        res = self.client.get(AIRPORTS_URL)

        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airport_forbidden_if_not_admin(self):
        payload = {"name": "Test Airport", "closest_big_city": "Test City"}
        res = self.client.post(AIRPORTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            "admin@test.com", "testpass"
        )
        self.client.force_authenticate(self.admin_user)

    def test_create_airport_success(self):
        payload = {"name": "Test Airport", "closest_big_city": "Test City"}
        res = self.client.post(AIRPORTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airport = Airport.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(airport, key))


class FlightModelTests(TestCase):
    def test_flight_str(self):
        flight = sample_flight()
        expected_str = f"{flight.route} on {flight.departure_time}"
        self.assertEqual(str(flight), expected_str)

    def test_validate_departure_time(self):
        with self.assertRaises(ValidationError):
            sample_flight(departure_time=timezone.now() - timedelta(days=1))

    def test_validate_arrival_time(self):
        with self.assertRaises(ValidationError):
            sample_flight(
                departure_time=timezone.now() + timedelta(days=1),
                arrival_time=(timezone.now() + timedelta(days=1) - timedelta(hours=1)),
            )


class TicketModelTests(TestCase):
    def setUp(self):
        self.flight = sample_flight()
        self.user = get_user_model().objects.create_user("test@test.com", "testpass")
        self.order = Order.objects.create(user=self.user)

    def test_create_ticket_with_valid_seat(self):
        ticket = Ticket.objects.create(
            row=1, seat=1, flight=self.flight, order=self.order
        )
        self.assertEqual(str(ticket), f"Ticket for " f"Flight {self.flight} - Seat 1-1")

    def test_validate_invalid_row(self):
        """Test that validation error is raised for invalid row number"""
        with self.assertRaises(ValidationError):
            Ticket.objects.create(
                row=100,  # Invalid row number
                seat=1,
                flight=self.flight,
                order=self.order,
            )

    def test_validate_invalid_seat(self):
        with self.assertRaises(ValidationError):
            Ticket.objects.create(
                row=1,
                seat=100,  # Invalid seat number
                flight=self.flight,
                order=self.order,
            )

    def test_unique_seat_constraint(self):
        Ticket.objects.create(row=1, seat=1, flight=self.flight, order=self.order)
        with self.assertRaises(ValidationError):
            Ticket.objects.create(
                row=1,
                seat=1,  # Same seat, should raise error
                flight=self.flight,
                order=self.order,
            )


class OrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@test.com", "testpass")
        self.client.force_authenticate(self.user)
        self.flight = sample_flight()

    def test_create_order_with_ticket(self):
        payload = {"ticket": {"row": 1, "seat": 1, "flight": self.flight.id}}
        res = self.client.post(ORDERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=res.data["id"])
        self.assertEqual(order.user, self.user)
        ticket = Ticket.objects.get(order=order)
        self.assertEqual(ticket.row, payload["ticket"]["row"])
        self.assertEqual(ticket.seat, payload["ticket"]["seat"])
        self.assertEqual(ticket.flight, self.flight)

    def test_list_user_orders(self):
        other_user = get_user_model().objects.create_user("other@test.com", "testpass")
        Order.objects.create(user=other_user)
        Order.objects.create(user=self.user)
        Order.objects.create(user=self.user)

        res = self.client.get(ORDERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)  # Should only see own orders
