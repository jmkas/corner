from django.contrib.auth.models import User
from reservation.serializers import RoomSerializer, ReservationSerializer
from reservation.models import RoomModel
from rest_framework.test import APITestCase


class TestRoomSerializer(APITestCase):
    def setUp(self):
        self.data = {"name": "Test_1", "location": "Test loc", "capacity": 1}
        RoomModel.objects.create(name="Test_1", location="Test loc", capacity=1)

    def test_add_room_with_same_name(self):
        ser = RoomSerializer(data=self.data)
        self.assertFalse(ser.is_valid())

    def test_add_room_with_zero_capacity(self):
        data = self.data
        data['capacity'] = 0
        ser = RoomSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_add_unique_room(self):
        data = self.data
        data['name'] = "Test_2"
        ser = RoomSerializer(data=data)
        self.assertTrue(ser.is_valid())


class TestReservationSerializer(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test', password="passwordTesting.123")
        User.objects.create_user(username='test2', password="passwordTesting.123")
        RoomModel.objects.create(name="Test_1", location="Test loc", capacity=3)
        self.data = {"title": "Test_1", "room": 1, "date_from": "2020-01-01 08:00", "date_to": "2020-01-01 10:00",
                     "employees": [2], "guests_count": 0, "owner": 1}

    def test_add_reservation(self):
        ser = ReservationSerializer(data=self.data)
        self.assertTrue(ser.is_valid())

    def test_with_more_capacity(self):
        data = self.data
        data['guests_count'] = 2
        ser = ReservationSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_with_equal_dates(self):
        data = self.data
        data['date_to'] = "2020-01-01 08:00"
        ser = ReservationSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_date_from_bigger(self):
        data = self.data
        data['date_from'] = "2020-01-01 11:00"
        ser = ReservationSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_room_not_available(self):
        ser = ReservationSerializer(data=self.data)
        if ser.is_valid():
            ser.save()
        data = self.data
        data["date_from"] = "2020-01-01 09:30"
        data["date_to"] = "2020-01-01 10:30"
        ser = ReservationSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_room_available(self):
        ser = ReservationSerializer(data=self.data)
        if ser.is_valid():
            ser.save()
        data = self.data
        data["date_from"] = "2020-01-01 10:00"
        data["date_to"] = "2020-01-01 10:30"
        ser = ReservationSerializer(data=data)
        self.assertTrue(ser.is_valid())

    def test_with_no_employees(self):
        data = self.data
        data['employees'] = []
        ser = ReservationSerializer(data=data)
        self.assertTrue(ser.is_valid())

    def test_with_no_owner(self):
        data = self.data
        del data['owner']
        ser = ReservationSerializer(data=data)
        self.assertFalse(ser.is_valid())