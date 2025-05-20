from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from django.shortcuts import get_object_or_404
from airport.models import AirplaneType


class AirportBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    closest_big_city: str = Field(..., min_length=1, max_length=100)


class AirportCreate(AirportBase):
    pass


class AirportResponse(AirportBase):
    id: int
    image: Optional[str] = None

    class Config:
        from_attributes = True


class RouteBase(BaseModel):
    source_id: int
    destination_id: int
    distance: int = Field(..., gt=0)


class RouteCreate(RouteBase):
    pass


class RouteResponse(RouteBase):
    id: int
    source: AirportResponse
    destination: AirportResponse

    class Config:
        from_attributes = True


class AirplaneTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class AirplaneTypeCreate(AirplaneTypeBase):
    pass


class AirplaneTypeResponse(AirplaneTypeBase):
    id: int

    class Config:
        from_attributes = True


class AirplaneBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    rows: int = Field(..., gt=0)
    seats_in_row: int = Field(..., gt=0)
    airplane_type_id: int

    @validator('airplane_type_id')
    def validate_airplane_type_exists(cls, v):
        try:
            AirplaneType.objects.get(id=v)
        except AirplaneType.DoesNotExist:
            raise ValueError(f"AirplaneType with id {v} does not exist")
        return v


class AirplaneCreate(AirplaneBase):
    pass


class AirplaneResponse(AirplaneBase):
    id: int
    image: Optional[str] = None
    capacity: int

    class Config:
        from_attributes = True


class CrewBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)


class CrewCreate(CrewBase):
    pass


class CrewResponse(CrewBase):
    id: int
    full_name: str

    class Config:
        from_attributes = True


class FlightBase(BaseModel):
    route_id: int
    airplane_id: int
    departure_time: datetime
    arrival_time: datetime
    crew_ids: List[int]

    @validator('arrival_time')
    def arrival_time_must_be_after_departure(cls, v, values):
        if 'departure_time' in values and v <= values['departure_time']:
            raise ValueError('Arrival time must be after departure time')
        return v


class FlightCreate(FlightBase):
    pass


class FlightResponse(FlightBase):
    id: int
    route: RouteResponse
    airplane: AirplaneResponse
    crew: List[CrewResponse]

    class Config:
        from_attributes = True


class TicketBase(BaseModel):
    row: int = Field(..., gt=0)
    seat: int = Field(..., gt=0)
    flight_id: int


class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    tickets: List[TicketCreate]


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    user_id: int
    tickets: List[TicketResponse]

    class Config:
        from_attributes = True
