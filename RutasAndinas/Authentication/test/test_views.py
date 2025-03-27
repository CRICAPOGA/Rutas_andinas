import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from Users.models import Role

@pytest.mark.django_db
def test_login_view(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert "login.html" in [t.name for t in response.templates]

@pytest.mark.django_db
def test_login_auth_success(client):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    
    response = client.post(reverse('login_auth'), {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert "index.html" in [t.name for t in response.templates]

@pytest.mark.django_db
def test_login_auth_fail(client):
    response = client.post(reverse('login_auth'), {'username': 'wronguser', 'password': 'wrongpass'})
    assert response.status_code == 200
    assert "login.html" in [t.name for t in response.templates]
    assert "Credenciales incorrectas" in response.content.decode()

@pytest.mark.django_db
def test_logout_view(client):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    client.login(username="testuser", password="testpassword")

    response = client.get(reverse('logout'))
    assert response.status_code == 200
    assert "login.html" in [t.name for t in response.templates]

@pytest.mark.django_db
def test_register_view_get(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200
    assert "register.html" in [t.name for t in response.templates]

@pytest.mark.django_db
def test_register_view_post(client):
    Role.objects.create(role="User")
    response = client.post(reverse('register'), {
        'name': 'Test',
        'last_name': 'User',
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    })
    
    assert response.status_code == 302  # Redirección al login
    assert reverse('login') in response.url
    User = get_user_model()
    assert User.objects.filter(username="testuser").exists()
