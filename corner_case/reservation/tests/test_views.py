from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
import json
from reservation.serializers import ReservationSerializer
from reservation.models import RoomModel


class TestRoomView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password="passwordTesting.123")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()
        self.url = reverse("reservation:rooms_view")
        self.data = {"name": "Test_1", "location": "Test loc", "capacity": 1}
        RoomModel.objects.create(name="Test_1", location="Test loc", capacity=1)

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_room(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_get_room_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_room(self):
        data = self.data
        data['name'] = "Test_2"
        self.client.post(self.url, data=self.data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_post_room_with_duplicate_name(self):
        data = self.data
        data['name'] = "Test_1"
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_room(self):
        data = {"name": self.data['name']}
        response = self.client.delete(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestReservationListView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testAdmin', password="passwordTesting.123")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()
        self.url = reverse("reservation:reservation_list_view")
        self.data = {"title": "Test_1", "room": 1, "date_from": "2020-01-01 08:00", "date_to": "2020-01-01 10:00",
                     'owner': 1, "employees": [], "guests_count": 2}
        RoomModel.objects.create(name="Test_1", location="Test loc", capacity=5)
        ser = ReservationSerializer(data=self.data)
        ser.is_valid()
        ser.save()

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_reservation(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_get_reservation_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_reservation(self):
        data = self.data
        data['date_from'] = "2020-01-01 10:00"
        data['date_to'] = "2020-01-01 11:00"
        self.client.post(self.url, data=self.data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_post_room_when_room_not_available(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestReservationDetailView(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test', password="passwordTesting.123")
        self.user = User.objects.create_user(username='test_2', password="passwordTesting.123")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()
        self.data = {"title": "Test_1", "room": 1, "date_from": "2020-01-01 08:00", "date_to": "2020-01-01 10:00",
                     'owner': 2, "employees": [], "guests_count": 2}

        RoomModel.objects.create(name="Test_1", location="Test loc", capacity=5)

        ser = ReservationSerializer(data=self.data)
        ser.is_valid()
        ser.save()
        self.url = reverse("reservation:reservation_detail_view", kwargs={'pk': ser.data['id']})

        data = self.data
        data['owner'] = 1
        data['date_from'] = "2020-01-03 08:00"
        data['date_to'] = "2020-01-03 10:00"
        ser = ReservationSerializer(data=data)
        ser.is_valid()
        ser.save()
        self.url2 = reverse("reservation:reservation_detail_view", kwargs={'pk': ser.data['id']})

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_reservations(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reservations_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_reservation(self):
        data = self.data
        data['date_from'] = "2020-01-02 10:00"
        data['date_to'] = "2020-01-02 11:00"
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_reservation_not_owner(self):
        data = self.data
        data['date_from'] = "2020-01-04 10:00"
        data['date_to'] = "2020-01-04 11:00"
        response = self.client.put(self.url2, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_reservation(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_reservation_not_owner(self):
        response = self.client.delete(self.url2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
