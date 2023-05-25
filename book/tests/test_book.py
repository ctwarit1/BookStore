import pytest
from rest_framework.reverse import reverse


@pytest.fixture
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


class TestBook:

    #                                      successful test cases
    #                                successful test case for post book
    @pytest.mark.django_db
    def test_post_book_successful(self, client, django_user_model, login_user):
        """Test for post book"""
        token = login_user
        post_book = {
            "title": "new book",
            "author": "twarit",
            "price": "200",
            "quantity": "3",
        }

        url = reverse('book-list')
        response = client.post(url, post_book, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    #                                unsuccessful test case for post book
    @pytest.mark.django_db
    def test_post_book_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for post book"""
        token = login_user
        post_book = {
            "title": "new book",
            "author": "twarit",
            "price": "200",
            "quantity": "",
        }

        url = reverse('book-list')
        response = client.post(url, post_book, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    #                                successful test case for get book
    @pytest.mark.django_db
    def test_get_book_successful(self, client, django_user_model, login_user):
        """Test for get book"""
        token = login_user
        post_book = {
            "title": "new book",
            "author": "twarit",
            "price": "200",
            "quantity": "3",
        }
        url = reverse('book-list')
        response = client.post(url, post_book, HTTP_TOKEN=token, content_type='application/json')
        url = reverse('book-list')
        response = client.get(url, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 202

    #                                unsuccessful test case for get book
    @pytest.mark.django_db
    def test_get_book_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for get book"""
        token = login_user
        post_book = {
            "title": "new book",
            "author": "twarit",
            "price": "200",
            "quantity": "3",
        }
        url = reverse('book-list')
        response = client.post(url, post_book, HTTP_TOKEN=token, content_type='application/json')
        url = reverse('book-list')
        response = client.get(url, content_type='application/json')
        assert response.status_code == 400

    #                                successful test case for update book
    @pytest.mark.django_db
    def test_update_book_successful(self, client, django_user_model, login_user):
        """Test for update book"""
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
        update_book = {
            "title": "book",
            "author": "twarit",
            "price": "100",
            "quantity": "3",
        }
        url = reverse('book-detail', args=[book_id])
        response = client.put(url, update_book, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    #                                unuccessful test case for update book
    @pytest.mark.django_db
    def test_update_book_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for update book"""
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
        update_book = {
            "title": "book",
            "author": "twarit",
            "price": "100",
            "quantity": "",
        }
        url = reverse('book-detail', args=[book_id])
        response = client.put(url, update_book, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    #                                successful test case for delete book
    @pytest.mark.django_db
    def test_delete_book_successful(self, client, django_user_model, login_user):
        """Test for delete book"""
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
        url = reverse('book-detail', args=[book_id])
        response = client.delete(url, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 200

    #                                unsuccessful test case for delete book
    @pytest.mark.django_db
    def test_delete_book_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for delete book"""
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
        url = reverse('book-detail', args=[book_id])
        response = client.put(url, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400
