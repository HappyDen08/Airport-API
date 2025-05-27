
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from functools import wraps





# Airport schemas
airport_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["name", "closest_big_city"],
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Airport ID"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the airport"),
        "closest_big_city": openapi.Schema(type=openapi.TYPE_STRING, description="Nearest major city to the airport"),
        "image": openapi.Schema(type=openapi.TYPE_STRING, description="URL of the airport image"),
    },
)

# AirplaneType schemas
airplane_type_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["name"],
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Airplane type ID"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the airplane type"),
    },
)

# Airplane schemas
airplane_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["name", "rows", "seats_in_row", "airplane_type"],
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Airplane ID"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the airplane"),
        "rows": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of rows in the airplane"),
        "seats_in_row": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of seats in each row"),
        "capacity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Total number of seats"),
        "image": openapi.Schema(type=openapi.TYPE_STRING, description="URL of the airplane image"),
        "airplane_type": airplane_type_schema,
    },
)

# Crew schemas
crew_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["first_name", "last_name"],
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Crew member ID"),
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="First name of the crew member"),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last name of the crew member"),
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, description="Full name of the crew member"),
    },
)

# Route schemas
route_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["source", "destination", "distance"],
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Route ID"),
        "source": airport_schema,
        "destination": airport_schema,
        "distance": openapi.Schema(type=openapi.TYPE_INTEGER, description="Distance between airports in kilometers"),
    },
)

# Flight schemas
flight_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["route", "airplane", "departure_time", "arrival_time", "crew"],
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Flight ID"),
        "route": route_schema,
        "airplane": airplane_schema,
        "departure_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Scheduled departure time"),
        "arrival_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Scheduled arrival time"),
        "crew": openapi.Schema(type=openapi.TYPE_ARRAY, items=crew_schema, description="List of crew members"),
    },
)

# Ticket schemas
ticket_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["row", "seat", "flight"],
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Ticket ID"),
        "row": openapi.Schema(type=openapi.TYPE_INTEGER, description="Row number in the airplane"),
        "seat": openapi.Schema(type=openapi.TYPE_INTEGER, description="Seat number in the row"),
        "flight": flight_schema,
        "order": openapi.Schema(type=openapi.TYPE_INTEGER, description="Order ID"),
    },
)

# Order schemas
order_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["tickets"],
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Order ID"),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Order creation timestamp"),
        "user": openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID"),
        "tickets": openapi.Schema(type=openapi.TYPE_ARRAY, items=ticket_schema, description="List of tickets"),
    },
)

# Error response schema
error_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
    },
)

# View decorators
def airport_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Airport operations",
        responses={
            200: openapi.Schema(type=openapi.TYPE_ARRAY, items=airport_schema),
            201: airport_schema,
            400: error_response_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def airplane_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Airplane operations",
        responses={
            200: openapi.Schema(type=openapi.TYPE_ARRAY, items=airplane_schema),
            201: airplane_schema,
            400: error_response_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def flight_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Flight operations",
        responses={
            200: openapi.Schema(type=openapi.TYPE_ARRAY, items=flight_schema),
            201: flight_schema,
            400: error_response_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def ticket_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Ticket operations",
        responses={
            200: openapi.Schema(type=openapi.TYPE_ARRAY, items=ticket_schema),
            201: ticket_schema,
            400: error_response_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def order_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Order operations",
        responses={
            200: openapi.Schema(type=openapi.TYPE_ARRAY, items=order_schema),
            201: order_schema,
            400: error_response_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
