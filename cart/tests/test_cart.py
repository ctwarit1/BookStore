import pytest
from rest_framework.reverse import reverse


@pytest.fixture()
def login_user(client, django_user_model):
    user_data = {
        "first_name": "twarit",
        "last_name": "chokniwal",
        "username": "ctwarit",
        "email": "ctwarit1@gmail.com",
        "password": "1234",
        "phone": "987654321",
        "is_superuser": True,
    }
    url = reverse('user')
    response = client.post(url, user_data)
    login_data = {
        "username": "ctwarit",
        "password": "1234"
    }
    url = reverse('login')
    response = client.post(url, login_data)
    return response.data.get("data")


@pytest.fixture()
def post_book(client, django_user_model, login_user):
    token = login_user
    post_book = {
        "title": "new book",
        "author": "twarit",
        "price": "200",
        "quantity": "3",
    }

    url = reverse('book-list')
    response = client.post(url, post_book, HTTP_TOKEN=token, content_type='application/json')
    book_id = response.data["data"]["id"]
    return book_id


class TestCart:

    @pytest.mark.django_db
    def test_create_cart_successful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_create_cart_unsuccessful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_get_cart_successful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        url = reverse('cart-list')
        response = client.get(url, HTTP_TOKEN=token, content_type='application/json')

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_cart_unsuccessful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        url = reverse('cart-list')
        response = client.get(url, content_type='application/json')

        assert response.status_code == 400

    @pytest.mark.django_db
    def test_delete_cart_successful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_TOKEN=token, content_type='application/json')
        cart_id = response.data["data"]["items"][0]["cart"]
        url = reverse('cart-detail', args=[cart_id])
        response = client.delete(url, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_delete_cart_unsuccessful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_TOKEN=token, content_type='application/json')
        cart_id = response.data["data"]["items"][0]["cart"]
        url = reverse('cart-detail', args=[cart_id])
        response = client.delete(url, content_type='application/json')
        assert response.status_code == 400


class TestOrder:

    @pytest.mark.django_db
    def test_post_order_successful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_TOKEN=token, content_type='application/json')
        cart_id = response.data["data"]["id"]
        url = reverse('order-list')
        response = client.post(url, {"cart": cart_id}, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_post_order_unsuccessful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_TOKEN=token, content_type='application/json')
        cart_id = response.data["data"]
        url = reverse('order-list')
        response = client.post(url, {"cart": cart_id}, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_get_order_successful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_TOKEN=token, content_type='application/json')
        url = reverse('order-list')
        response = client.get(url, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_get_order_unsuccessful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_TOKEN=token, content_type='application/json')
        url = reverse('order-list')
        response = client.get(url, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_delete_order_successful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_TOKEN=token, content_type='application/json')
        cart_id = response.data["data"]["id"]
        url = reverse('order-detail', args=[cart_id])
        response = client.delete(url, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_delete_order_unsuccessful(self, client, django_user_model, login_user, post_book):
        token = login_user
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_TOKEN=token, content_type='application/json')
        cart_id = response.data["data"]
        url = reverse('order-detail', args=[cart_id])
        response = client.delete(url, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400
