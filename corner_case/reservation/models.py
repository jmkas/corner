from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

# Create your models here.
class RoomModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.TextField()
    capacity = models.IntegerField(validators=[MinValueValidator(1)])


class ReservationModel(models.Model):
    title = models.CharField(max_length=255)
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants', blank=True)
    guests_count = models.IntegerField()
