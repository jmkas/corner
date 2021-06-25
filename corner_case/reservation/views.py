from reservation.models import RoomModel, ReservationModel
from reservation.serializers import RoomSerializer, ReservationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from reservation.permissions import IsOwnerOrReadOnly

from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema

class RoomView(APIView):
    """
    Rooms
    Only logged in users can get info about all rooms and create or delete rooms
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoomSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
    #
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get_object(self, room_name):
        try:
            return RoomModel.objects.get(name=room_name)
        except RoomModel.DoesNotExist:
            raise Http404

    def get(self, format=None):
        data = RoomModel.objects.all()
        serializer = RoomSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        room = self.get_object(request.data['name'])
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationListView(APIView):
    """
    Reservation list
    Only logged in users can get info about all reservations and create new ones
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
    #
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get(self, format=None):
        data = ReservationModel.objects.all()
        serializer = ReservationSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data._mutable = True
        data = request.data
        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationDetailView(APIView):
    """
    Reservation detail
    Only logged in users can get, change info or delete specific reservation
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ReservationSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
    #
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get_object(self, reservation_id):
        try:
            return ReservationModel.objects.get(id=reservation_id)
        except ReservationModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = ReservationSerializer(data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        reservation = self.get_object(pk)
        self.check_object_permissions(self.request, reservation)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        reservation = self.get_object(pk)
        self.check_object_permissions(self.request, reservation)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
