import pytest
from rest_framework.reverse import reverse


class TestUser:

    @pytest.mark.django_db
    def test_reg_successful(self, client, django_user_model):
        user_data = {
            "first_name": "twarit",
            "last_name": "chokniwal",
            "username": "ctwarit",
            "email": "ctwarit1@gmail.com",
            "password": "1234",
            "phone": "987654321"
        }
        url = reverse('user')
        response = client.post(url, user_data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_reg_unsuccessful(self, client, django_user_model):
        user_data = {
            "first_name": "twarit",
            "last_name": "chokniwal",
            "username": "",
            "email": "ctwarit1@gmail.com",
            "password": "1234",
            "phone": "987654321"
        }
        url = reverse('user')
        response = client.post(url, user_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_login_successful(self, client, django_user_model):
        user_data = {
            "first_name": "twarit",
            "last_name": "chokniwal",
            "username": "ctwarit",
            "email": "ctwarit1@gmail.com",
            "password": "1234",
            "phone": "987654321"
        }
        url = reverse('user')
        response = client.post(url, user_data)
        login_data = {
            "username": "ctwarit",
            "password": "1234"
        }
        url = reverse('login')
        response = client.post(url, login_data)
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_login_unsuccessful(self, client, django_user_model):
        user_data = {
            "first_name": "twarit",
            "last_name": "chokniwal",
            "username": "ctwarit",
            "email": "ctwarit1@gmail.com",
            "password": "1234",
            "phone": "987654321"
        }
        url = reverse('user')
        response = client.post(url, user_data)
        login_data = {
            "username": "ctwarit",
            "password": ""
        }
        url = reverse('login')
        response = client.post(url, login_data)
        assert response.status_code == 400