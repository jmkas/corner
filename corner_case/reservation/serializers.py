from rest_framework import serializers
from reservation.models import RoomModel, ReservationModel


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomModel
        fields = ['name', 'location', 'capacity']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationModel
        fields = ['id', 'title', 'room', 'date_from', 'date_to', 'employees', 'owner', 'guests_count']

    def in_between(self, now, start, end):
        if start < end:
            return start <= now < end
        elif end < start:
            return start <= now or now < end
        else:
            return True

    def validate(self, value):
        if value['date_to'] < value['date_from']:
            raise serializers.ValidationError('Date from must be earlier than date to')
        if value['date_to'] == value['date_from']:
            raise serializers.ValidationError('Dates can not be equal to each other')
        room = RoomModel.objects.filter(id=value['room'].id).first()
        n = len(value['employees']) + value['guests_count'] + 1
        if room.capacity < n:
            raise serializers.ValidationError("Too many occupants")
        reserv = ReservationModel.objects.filter(room=value['room'].id, date_from__year=value['date_from'].year,
                                                 date_from__month=value['date_from'].month,
                                                 date_from__day=value['date_from'].day).all()
        for i in reserv:
            if self.in_between(value['date_from'], i.date_from, i.date_to) or \
                    self.in_between(value['date_to'], i.date_from, i.date_to):
                raise serializers.ValidationError('Room is not available at selected time')
        return value
