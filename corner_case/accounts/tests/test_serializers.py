from accounts.serializers import UserSerializer
from rest_framework.test import APITestCase


class TestAccountsSerializer(APITestCase):
    def test_normal_serialization_validation(self):
        data = {'username': 'test', 'password': 'pas123123'}
        ser = UserSerializer(data=data)
        self.assertTrue(ser.is_valid())

    def test_serialization_validation_without_password(self):
        data = {'username': 'test'}
        ser = UserSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_validation_without_username(self):
        data = {'password': 'pas123123'}
        ser = UserSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_validation_without_any_data(self):
        data = {}
        ser = UserSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_create(self):
        data = {'username': 'test', 'password': 'pas123123'}
        ser = UserSerializer(data=data)
        ser.is_valid()
        ser.save()
        self.assertEqual(ser.data.keys(), {"id", "username"})
