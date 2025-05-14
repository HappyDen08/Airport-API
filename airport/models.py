from django.db import models
from rest_framework.exceptions import ValidationError

from user.models import User


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Airport, related_name="departures", on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, related_name="arrivals", on_delete=models.CASCADE)
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} → {self.destination}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name



class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"id {self.id} {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew)

    def __str__(self):
        return f"{self.route} on {self.departure_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("flight", "row", "seat")

    def __str__(self):
        return f"Ticket for Flight {self.flight} - Seat {self.row}-{self.seat}"

    @staticmethod
    def validate_row(flight, row):
        airplane = flight.airplane
        if not 1 <= row <= airplane.rows:
            raise ValidationError(
                f"Row number must be between 1 and {airplane.rows}"
            )

    @staticmethod
    def validate_seat(flight, seat, row):
        airplane = flight.airplane
        if not 1 <= seat <= airplane.seats_in_row:
            raise ValidationError(
                f"Seat number must be between 1 and {airplane.seats_in_row}"
            )

    def clean(self):
        Ticket.validate_row(self.flight, self.row)
        Ticket.validate_seat(self.flight, self.seat, self.row)

        if Ticket.objects.filter(
            flight=self.flight,
            row=self.row,
            seat=self.seat
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                "This seat already reserved"
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
