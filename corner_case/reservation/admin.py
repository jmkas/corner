from django.contrib import admin
from reservation.models import RoomModel, ReservationModel
# Register your models here.

admin.site.register(RoomModel)
admin.site.register(ReservationModel)
