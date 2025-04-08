import pytest
from django.urls import reverse
from Plans.models import Plan, Category
from Users.models import Role
from django.contrib.auth import get_user_model

@pytest.fixture
def authenticated_client(client, db):
    # Crear rol Empleado
    role = Role.objects.create(role="Empleado")
    
    # Crear usuario con ese rol
    User = get_user_model()
    user = User.objects.create_user(
        username="empleado",
        password="password123",
        role_id=role
    )

    # Loguear al usuario
    client.login(username="empleado", password="password123")
    return client

@pytest.mark.django_db
def test_list_view(authenticated_client):
    url = reverse('list')
    response = authenticated_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_plan_view_get(authenticated_client):
    url = reverse('createPlan')
    response = authenticated_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_plan_view_post(client):
    url = reverse('createPlan')
    data = {
        'nombre': 'Plan de prueba',
        'descripcion': 'Descripción de prueba',
        'precio': 1000
    }
    response = client.post(url, data)
    assert response.status_code in (200, 302)  # Puede redirigir si es exitoso


@pytest.mark.django_db
def test_catalog_view(client):
    url = reverse('catalog')
    response = client.get(url)
    assert response.status_code == 200
