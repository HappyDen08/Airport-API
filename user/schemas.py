from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from functools import wraps


# User schemas
register_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=[
        "email",
        "password",
        "first_name",
        "last_name",
    ],
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            format="email",
            description="Email address (used as username)"
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Password",
            min_length=5
        ),
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="First name"
        ),
        "last_name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Last name"
        ),
    },
)

login_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["email", "password"],
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            format="email",
            description="Email address"
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Password"
        ),
    },
)

user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="User ID"
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            format="email",
            description="Email address"
        ),
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="First name"
        ),
        "last_name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Last name"
        ),
        "is_staff": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="Whether the user is a staff member"
        ),
    },
)

token_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Access token"
        ),
        "refresh": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Refresh token"
        ),
    },
)

refresh_token_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["refresh"],
    properties={
        "refresh": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Refresh token"
        ),
    },
)

verify_token_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["token"],
    properties={
        "token": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Token to verify"
        ),
    },
)

error_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "error": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Error message"
        ),
    },
)

success_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "message": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Success message"
        ),
    },
)


# View decorators
def register_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Register a new user account",
        request_body=register_schema,
        responses={
            201: user_schema,
            400: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def login_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Login with email and password",
        request_body=login_schema,
        responses={
            200: token_schema,
            400: error_response_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def user_detail_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Get current user profile information",
        responses={
            200: user_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def refresh_token_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Refresh access token using refresh token",
        request_body=refresh_token_schema,
        responses={
            200: token_schema,
            400: error_response_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def verify_token_view_schema(func):
    @wraps(func)
    @swagger_auto_schema(
        operation_description="Verify token validity",
        request_body=verify_token_schema,
        responses={
            200: success_response_schema,
            400: error_response_schema,
            401: error_response_schema,
        },
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper 