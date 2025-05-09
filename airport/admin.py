from django.contrib import admin

from airport.models import (Airport,
                            Route,
                            AirplaneType,
                            Airplane,
                            Crew,
                            Flight,
                            Order,
                            Ticket)


admin.register(Airport)
admin.register(Route)
admin.register(AirplaneType)
admin.register(Airplane)
admin.register(Crew)
admin.register(Flight)
admin.register(Order)
admin.register(Ticket)
