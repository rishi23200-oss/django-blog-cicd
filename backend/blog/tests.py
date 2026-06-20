import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import Author, Post


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    u = User.objects.create_user(username='testuser', password='testpass123')
    Author.objects.create(user=u, bio='Test author')
    return u


@pytest.fixture
def auth_client(api_client, user):
    response = api_client.post('/api/token/', {'username': 'testuser', 'password': 'testpass123'})
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.mark.django_db
def test_health_check(api_client):
    response = api_client.get('/health/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}


@pytest.mark.django_db
def test_readiness_check(api_client):
    response = api_client.get('/readiness/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ready'}


@pytest.mark.django_db
def test_get_token(api_client, user):
    response = api_client.post('/api/token/', {'username': 'testuser', 'password': 'testpass123'})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_list_posts_unauthenticated(api_client):
    response = api_client.get('/posts/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_post_unauthenticated(api_client):
    response = api_client.post('/posts/', {'title': 'Test', 'content': 'Hello'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_post_authenticated(auth_client):
    response = auth_client.post('/posts/', {'title': 'My Post', 'content': 'Some content'})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'My Post'


@pytest.mark.django_db
def test_add_comment_authenticated(auth_client, user):
    author = Author.objects.get(user=user)
    post = Post.objects.create(title='P', content='C', author=author)
    response = auth_client.post(f'/posts/{post.id}/comments/', {'content': 'Nice post!'})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_list_comments(api_client, user):
    author = Author.objects.get(user=user)
    post = Post.objects.create(title='P', content='C', author=author)
    response = api_client.get(f'/posts/{post.id}/comments/')
    assert response.status_code == status.HTTP_200_OK
