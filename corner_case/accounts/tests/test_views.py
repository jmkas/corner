from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
import json


class TestCreateUserView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testAdmin', password="passwordTesting.123")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()
        self.url = reverse("accounts:reg_view")

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_user_create_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_without_username(self):
        data = {"password": "testPassword.1"}
        response = self.client.post(path=self.url, data=data)
        self.assertIsNotNone(response.json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_without_password(self):
        data = {'username': 'test'}
        response = self.client.post(path=self.url, data=data)
        self.assertIsNotNone(response.json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_without_any_data(self):
        response = self.client.post(path=self.url)
        self.assertIsNotNone(response.json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_with_data(self):
        data = {'username': 'test', "password": "testPassword.1"}
        response = self.client.post(path=self.url, data=data)
        self.assertIsNotNone(response.json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_dublicate_creation(self):
        data = {'username': 'tests', "password": "testPassword.1"}
        self.client.post(path=self.url, data=data)
        response = self.client.post(path=self.url, data=data)
        self.assertIsNotNone(response.json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_not_allowed_create_methods(self):
        data = {'username': 'test', "password": "testPassword.1"}
        response_get = self.client.get(path=self.url)
        response_put = self.client.put(path=self.url, data=data)
        response_delete = self.client.delete(path=self.url)
        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestLogin(APITestCase):
    def setUp(self):
        self.url = reverse("accounts:login_view")
        self.data = {'username': 'testLogin', "password": "testPassword.1"}
        self.user = User.objects.create_user(username='testLogin', password="testPassword.1")

    def test_token_login(self):
        responce = self.client.post(self.url, data=self.data)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(responce.content).keys(), {'token'})

    def test_bad_password_login(self):
        self.data['password'] = "badPassword"
        responce = self.client.post(self.url, data=self.data)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(responce.content),
                         {'non_field_errors': ['Unable to log in with provided credentials.']})

    def test_bad_username_login(self):
        self.data = {'username': 'badLogin', "password": "testPassword.1"}
        responce = self.client.post(self.url, data=self.data)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(responce.content),
                         {'non_field_errors': ['Unable to log in with provided credentials.']})

    def test_no_data_login(self):
        self.data = {}
        responce = self.client.post(self.url, data=self.data)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(responce.content),
                         {'password': ['This field is required.'], 'username': ['This field is required.']})
